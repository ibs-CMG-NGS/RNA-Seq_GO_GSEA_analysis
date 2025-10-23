# =============================================================
# file: src/analysis/gsea_plot.py (필터링 기능 추가 버전)
# =============================================================
import argparse
import logging
import os
from pathlib import Path

import pandas as pd
from gseapy.plot import barplot, dotplot
from utils.FileFunctions import ensure_dir
from utils.config_utils import get_cfg, pick, resolve_path
from utils.logging_utils_environ import setup_logging

# --- 로그 설정 ---
# 이 함수는 PIPELINE_LOG_FILE 환경 변수를 확인하여
# 이미 존재하는 로그 파일을 사용하거나, 없으면 새로 만듭니다.
log, _ = setup_logging()

def create_gsea_plots_from_excel(
    excel_path: Path,
    output_plot_dir: Path,
    plot_formats: list,
    top_n_plots: int,
    fdr_cutoff: float
):
    """
    GSEA Excel 리포트의 모든 시트를 순회하며 요약 플롯을 생성합니다.
    """
    log.info(f"GSEA Excel 리포트로부터 플롯 생성을 시작합니다: {excel_path.name}")
    ensure_dir(str(output_plot_dir))

    try:
        xls = pd.ExcelFile(excel_path)
    except FileNotFoundError:
        log.error(f"입력 파일(Excel)을 찾을 수 없습니다: {excel_path}")
        return

    for sheet_name in xls.sheet_names:
        log.info(f"--- 시트 처리 중: '{sheet_name}' ---")
        gsea_df = pd.read_excel(xls, sheet_name=sheet_name)
        
        # FDR 기준으로 유의미한 결과 필터링
        significant_df = gsea_df[gsea_df['FDR q-val'] < fdr_cutoff].copy()
        
        if significant_df.empty:
            log.warning(f"'{sheet_name}' 시트에는 FDR < {fdr_cutoff} 기준을 만족하는 유의미한 결과가 없습니다. 플롯 생성을 건너뜁니다.")
            continue
            
        log.info(f"'{sheet_name}' 시트에서 {len(significant_df)}개의 유의미한 유전자 세트를 찾았습니다. 상위 {top_n_plots}개를 시각화합니다.")

        # --- Dot Plot 생성 ---
        try:
            dotplot_filename = f"dotplot_{sheet_name}.{plot_formats[0]}"
            dotplot(significant_df,
                    title=sheet_name,
                    column="FDR q-val",
                    top_term=top_n_plots,
                    ofname=str(output_plot_dir / dotplot_filename),
                    figsize=(8, 10),
                    cutoff=1.0)
            log.info(f"Dot plot 생성 완료: {dotplot_filename}")
        except Exception as e:
            log.error(f"'{sheet_name}' 시트의 Dot plot 생성 중 오류 발생: {e}")

        # --- Bar Plot 생성 ---
        try:
            if 'Adjusted P-value' not in significant_df.columns:
                significant_df['Adjusted P-value'] = significant_df['FDR q-val']
            
            barplot_filename = f"barplot_{sheet_name}.{plot_formats[0]}"
            barplot(significant_df,
                    ofname=str(output_plot_dir / barplot_filename),
                    top_term=top_n_plots,
                    cutoff=1.0)
            log.info(f"Bar plot 생성 완료: {barplot_filename}")
        except Exception as e:
            log.error(f"'{sheet_name}' 시트의 Bar plot 생성 중 오류 발생: {e}")
    
    log.info(f"✅ 모든 시트에 대한 GSEA 플롯 생성이 완료되었습니다. 결과 폴더: {output_plot_dir}")


def _parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Generate summary plots from a GSEA Excel report.")
    parser.add_argument("--config", required=True, help="Path to the main YAML configuration file.")
    parser.add_argument("--config-section", default="gsea_plot", help="The section in the YAML file to use.")
    return parser.parse_args(argv)


def _main(argv=None):
    args = _parse_args(argv)
    cfg_all = get_cfg(args.config)
    cfg = cfg_all.get(args.config_section, {})

    # YAML 설정에서 입력 Excel 파일 경로와 출력 디렉터리 경로를 가져옵니다.
    input_excel_paths = resolve_path(cli_path=None, cfg=cfg_all, config_key="gsea_input_excel", config_section=args.config_section)
    if not input_excel_paths:
        raise SystemExit("Error: 'gsea_input_excel'이 설정 파일에 정의되지 않았습니다.")
    
    output_plot_dir_paths = resolve_path(cli_path=None, cfg=cfg_all, config_key="gsea_plot_output_dir", config_section=args.config_section)
    if not output_plot_dir_paths:
        raise SystemExit("Error: 'gsea_plot_output_dir'이 설정 파일에 정의되지 않았습니다.")

    # 설정값 읽어오기
    plot_formats = pick(None, cfg, "plot_formats", ["png"])
    top_n = pick(None, cfg, "top_n_plots", 15)
    fdr_cutoff = pick(None, cfg, "fdr_cutoff", 0.25)

    create_gsea_plots_from_excel(
        excel_path=Path(input_excel_paths[0]),
        output_plot_dir=Path(output_plot_dir_paths[0]),
        plot_formats=plot_formats,
        top_n_plots=top_n,
        fdr_cutoff=fdr_cutoff
    )

if __name__ == "__main__":
    _main()