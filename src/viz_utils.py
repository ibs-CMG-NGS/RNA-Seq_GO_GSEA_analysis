import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import re

def plot_heatmap(pivot_df, title, output_path, pdf=None):
    plt.figure(figsize=(14, 6))
    sns.heatmap(pivot_df, annot=True, cmap='viridis' if 'p_val' in title else 'coolwarm', center=0 if 'avg' in title else 0.05)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight') # Save to PNG, ensuring everything is saved
    if pdf:
        pdf.savefig(plt.gcf(), bbox_inches='tight') # Save to PDF, also ensuring everything is saved
    plt.close(plt.gcf()) # Close the current figure object

def plot_dot_plot(log2fc_data, pval_data, title, plot_options: dict, save_path=None, pdf=None, gene_order=None):
    """
    log2FC와 p-value를 사용하여 Dot Plot을 생성합니다.
    - 색상: log2FC (bwr 컬러맵)
    - 크기: -log10(p-value)를 범주화하여 표현
    - y축 순서: gene_order 리스트에 따라 정렬
    """
    # 데이터 재구성
    log2fc_flat = log2fc_data.stack().reset_index(name='log2FC')
    pval_flat = pval_data.stack().reset_index(name='padj') # padj 컬럼 이름이 일치해야 함

    # 데이터 병합
    merge_cols = [log2fc_data.index.name, pval_data.columns.name] # e.g., ['gene', 'source']
    plot_df = pd.merge(log2fc_flat, pval_flat, on=merge_cols, how="left")

    # --- 설정값 불러오기 ---
    fig_size = plot_options.get("figure_size", (10, 8))
    xaxis_title = plot_options.get("xaxis_title", pval_data.columns.name or 'Condition')
    color_norm_tuple = tuple(plot_options.get("color_norm", (-2, 2)))
    size_map = plot_options.get("size_map", {
        'p < 0.001': 300,
        'p < 0.01': 200,
        'p < 0.05': 100,
        'p > 0.05': 20
    })
    # Dot outline options
    dot_outline_color = plot_options.get("dot_outline_color")
    dot_outline_width = plot_options.get("dot_outline_width", 0)
    edgecolor = dot_outline_color if dot_outline_color else 'none'
    linewidth = dot_outline_width if dot_outline_color else 0

    # Colorbar options
    colorbar_width = plot_options.get("colorbar_width", 0.02)
    colorbar_height_ratio = plot_options.get("colorbar_height_ratio", 0.5)
    colorbar_x_offset = plot_options.get("colorbar_x_offset", 0.06)
    colorbar_y_offset = plot_options.get("colorbar_y_offset", 0.05)
    colorbar_ticks = plot_options.get("colorbar_ticks")
    colorbar_ticklabels = plot_options.get("colorbar_ticklabels")

    # size_map에서 p-value 임계값과 카테고리 이름을 동적으로 추출
    # 예: 'p < 0.01' -> 0.01
    thresholds = sorted([float(re.search(r'[\d.]+', cat).group()) for cat in size_map if '<' in cat])

    # p-value를 config에 정의된 카테고리로 변환하는 함수
    def pval_to_category(p):
        for t in thresholds:
            if p <= t:
                return f'p < {t}'
        # 가장 큰 임계값보다 크면 'p > ...' 카테고리로 분류
        largest_threshold = max(thresholds) if thresholds else 0.05
        return f'p > {largest_threshold}'

    # 범례 순서 정렬을 위해 카테고리 순서 정의
    # size_map의 키 순서를 그대로 사용하여 범례 순서 정의
    p_category_order = sorted(size_map.keys(), key=lambda k: size_map[k])
    plot_df['p_category'] = plot_df['padj'].apply(pval_to_category)
    plot_df['p_category'] = pd.Categorical(plot_df['p_category'], categories=p_category_order, ordered=True)

    # y축 순서 지정을 위해 gene 컬럼을 Categorical 타입으로 변환
    gene_col_name = log2fc_data.index.name
    if gene_order and gene_col_name in plot_df.columns:
        plot_df[gene_col_name] = pd.Categorical(plot_df[gene_col_name], categories=gene_order, ordered=True)

    # size_map의 키를 p_category와 일치하도록 조정 (예: 'p < 0.01' -> 'p < 0.010')
    # 이는 pval_to_category가 float에서 생성한 문자열과 정확히 일치시키기 위함입니다.
    # 더 나은 방법은 정규식을 사용하여 키를 비교하는 것이지만, 현재 구조에서는 이 방식이 간단합니다.
    # 이 부분은 현재 코드에서 문제가 없으므로 그대로 둡니다.

    # --- 시각화 ---
    fig, ax = plt.subplots(figsize=fig_size)
    sns.scatterplot(
        data=plot_df,
        x=pval_data.columns.name,
        y=log2fc_data.index.name,
        hue='log2FC',
        size='p_category',  # 범례를 위해 카테고리 컬럼 사용
        sizes=size_map,     # 카테고리와 크기 매핑
        palette='bwr',
        hue_norm=color_norm_tuple,
        legend='auto',      # legend를 생성한 후 수동으로 관리 (Seaborn 0.11.0+에서는 'brief'가 더 적합할 수 있음)
        ax=ax,
        edgecolor=edgecolor, # 점 테두리 색상
        linewidth=linewidth  # 점 테두리 두께
    )
    # ax.margins() 대신 xlim으로 여백을 조절하여 점들이 잘리지 않게 합니다.
    # 카테고리 개수에 따라 여백을 동적으로 조절할 수 있습니다.
    ax.set_xlim(-0.5, len(ax.get_xticks()) - 0.5)
    plt.title(title, fontsize=16)
    plt.xlabel(xaxis_title)

    # --- 범례 및 컬러바 조정 ---
    # 기존 범례 가져오기 및 위치 조정
    h, l = ax.get_legend_handles_labels()
    # 'p_category' 레이블이 있는 인덱스를 찾고, 그 이후의 핸들과 레이블을 사용
    size_legend_handles = [handle for handle, label in zip(h, l) if label in p_category_order]
    size_legend_labels = [label for label in l if label in p_category_order]

    size_legend = ax.legend(size_legend_handles, size_legend_labels,
                            title="Adjusted P-value",
                            bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

    # 연속적인 컬러바 생성
    norm = plt.Normalize(color_norm_tuple[0], color_norm_tuple[1])
    sm = plt.cm.ScalarMappable(cmap="bwr", norm=norm)
    sm.set_array([])
    
    # 컬러바 위치 계산
    ax_pos = ax.get_position()
    cax = fig.add_axes([ax_pos.x1 + colorbar_x_offset, ax_pos.y0 + colorbar_y_offset, colorbar_width, ax_pos.height * colorbar_height_ratio])
    cb = fig.colorbar(sm, cax=cax, label='log2FC')
    if colorbar_ticks is not None:
        cb.set_ticks(colorbar_ticks)
    if colorbar_ticklabels is not None:
        cb.set_ticklabels(colorbar_ticklabels)

    plt.xticks(rotation=45, ha='right')
    # fig.tight_layout()은 add_axes와 충돌하여 경고를 발생시키므로 제거합니다.
    # 대신, 저장 시 bbox_inches='tight' 옵션을 사용하여 모든 요소가 포함되도록 합니다.
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    if pdf:
        pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)
