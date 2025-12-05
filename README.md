# RNA-Seq 후속 분석 파이프라인: GO 및 GSEA

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![English](https://img.shields.io/badge/README-English-blue)](README_EN.md)

RNA-Seq 차등 발현 분석 후 **Gene Ontology (GO) 농축 분석**과 **Gene Set Enrichment Analysis (GSEA)**를 수행하는 모듈화된 Python 파이프라인입니다.

## 🎯 주요 특징

- **🧩 모듈식 설계:** 독립적이고 재사용 가능한 분석 모듈
- **⚙️ 설정 기반:** YAML 파일로 재현 가능한 분석 수행
- **🐍 Snakemake 통합:** 병렬 처리 및 자동화된 워크플로우
- **📊 논문 수준 결과물:** 고품질 시각화 및 HTML 리포트

## 📋 목차

- [설치](#-설치)
- [빠른 시작](#-빠른-시작)
- [Snakemake 워크플로우](#-snakemake-워크플로우)
- [설정 파일](#-설정)
- [프로젝트 구조](#-프로젝트-구조)

## 🚀 설치

### 사전 요구사항
- Python 3.9 이상
- Conda 패키지 매니저 (권장)

### Conda를 사용한 설치

```bash
# 1. 저장소 복제
git clone https://github.com/ibs-CMG-NGS/RNA-Seq_GO_GSEA_analysis.git
cd RNA-Seq_GO_GSEA_analysis

# 2. Snakemake 환경 생성 및 활성화
conda env create -f snakemake_environment.yml
conda activate snakemake_env
```

## ⚡ 빠른 시작

### 옵션 1: 인터랙티브 분석 (노트북)

```bash
# Jupyter 시작
jupyter notebook

# 가이드 노트북 중 하나 열기:
# - notebooks/GO_Pipeline.ipynb (GO 농축 분석용)
# - notebooks/GSEA_Pipeline.ipynb (GSEA 분석용)
```

### 옵션 2: Snakemake 워크플로우 (권장)

**단일 샘플 분석:**
```bash
# GO 농축 분석
snakemake --snakefile workflow/Snakefile_GO \
    --configfile workflow/config/go_config.yaml \
    --cores 1

# GSEA 분석
snakemake --snakefile workflow/Snakefile_GSEA \
    --configfile workflow/config/gsea_config.yaml \
    --cores 1
```

**배치 분석 (여러 샘플 병렬 처리):**
```bash
# 설정 파일 편집
nano workflow/config/batch_go_config.yaml

# 배치 GO 분석 실행
snakemake --snakefile workflow/Snakefile_batch_GO \
    --configfile workflow/config/batch_go_config.yaml \
    --cores 4
```

자세한 사용법은 [Workflow README](workflow/README.md)를 참조하세요.

## 🐍 Snakemake 워크플로우

Snakemake는 재현성과 확장성을 제공하는 워크플로우 관리 시스템입니다.

### 주요 장점
- **자동 병렬화:** 독립적인 샘플을 자동으로 병렬 실행
- **의존성 추적:** 입력이 변경될 때만 단계를 재실행
- **에러 복구:** 실패 지점에서 재개
- **확장성:** 로컬에서 HPC 클러스터까지

### 기본 사용법

```bash
# Dry-run (실행될 내용 확인)
snakemake --snakefile workflow/Snakefile_GO \
    --configfile workflow/config/go_config.yaml \
    --dry-run

# 워크플로우 시각화 (graphviz 필요)
snakemake --snakefile workflow/Snakefile_GO \
    --configfile workflow/config/go_config.yaml \
    --dag | dot -Tpng > workflow_dag.png
```

### HPC 클러스터 실행 (SLURM)

```bash
snakemake --snakefile workflow/Snakefile_batch_GO \
    --configfile workflow/config/batch_go_config.yaml \
    --cluster "sbatch --time=02:00:00 --mem=16G" \
    --jobs 10
```

자세한 내용은 [Workflow README](workflow/README.md)를 참조하세요.

## ⚙️ 설정

모든 분석 파라미터는 YAML 파일로 관리됩니다.

### 설정 파일 구조

```
configs/
├── GO_pipeline_*.yaml          # GO 농축 분석 메인 설정
├── deg_comparison_*.yaml        # DEG 비교 분석 설정
├── gene_filter_*.yaml          # 유전자 필터링 분석 설정
├── genes_of_interest.txt       # 관심 유전자 리스트
├── README.md                   # 설정 파일 사용 가이드
└── legacy/                     # 구버전 설정 파일 (참고용)
```

### 설정 파일 예시

**GO 농축 분석 (`configs/GO_pipeline_Shank2.yaml`):**
```yaml
ROOT_DIR: "data/processed/Shank2"

data_loading:
  excel_path: "data/Shank2_DEG.xlsx"
  gene_col: "external_gene_name"
  log2fc_col: "log2.FC."
  padj_col: "P.adj"

filtering:
  padj_cutoff: 0.01
  log2fc_cutoff: 0.5
  direction: both

go_enrich:
  obo: "ref/go-basic.obo"
  gaf: "ref/goa_mouse.gaf"
  taxon: 10090
  alpha: 0.05
```

자세한 내용은 [configs/README.md](configs/README.md)를 참조하세요.

## 📁 프로젝트 구조

```
RNA-Seq_GO_GSEA_analysis/
├── configs/                      # YAML 설정 파일
│   ├── GO_pipeline_*.yaml       # GO 분석 설정
│   ├── deg_comparison_*.yaml    # DEG 비교 설정
│   ├── gene_filter_*.yaml       # 유전자 필터 설정
│   └── README.md                # 설정 가이드
├── workflow/                     # Snakemake 워크플로우
│   ├── Snakefile_GO             # GO 분석 워크플로우
│   ├── Snakefile_GSEA           # GSEA 분석 워크플로우
│   ├── Snakefile_batch_GO       # 배치 GO 분석
│   ├── config/                  # 워크플로우 설정
│   └── README.md                # 워크플로우 가이드
├── notebooks/                    # Jupyter 노트북
│   ├── GO_Pipeline.ipynb
│   └── GSEA_Pipeline.ipynb
├── src/                          # 소스 코드
│   └── analysis/                # 분석 모듈
│       ├── data_loading.py
│       ├── filtering.py
│       ├── go_enrich.py
│       ├── gsea_analysis.py
│       └── ...
├── data/                         # 입력 데이터 (gitignored)
├── results/                      # 분석 결과 (gitignored)
├── ref/                          # 참조 파일 (GO, GMT)
├── scripts/                      # 헬퍼 스크립트
├── environment.yml               # Conda 환경 설정
└── snakemake_environment.yml     # Snakemake 환경 설정
```

## 📊 분석 파이프라인

### GO 농축 분석 파이프라인

```
Excel 입력 → 데이터 로딩 → 필터링 → Volcano Plot → GO 농축 → 시각화 → 리포트
```

1. **데이터 로딩** - Excel 입력 파일 표준화
2. **필터링** - 통계적 임계값으로 유의미한 DEG 추출
3. **Volcano Plot** - 차등 발현 시각화
4. **GO 농축** - GOATOOLS를 사용한 GO term 농축 분석
5. **GO 시각화** - Bar/dot plot 생성
6. **리포트 생성** - HTML 리포트 컴파일

### GSEA 분석 파이프라인

```
Excel 입력 → 데이터 로딩 → GSEA 실행 → 시각화 → 리포트
```

**지원 모드:**
- **Pre-ranked GSEA:** DE 분석 결과에서 ranked list 사용 (빠름, 권장)
- **Classic GSEA:** Expression matrix와 샘플 그룹 정보 사용 (엄격)

## 📚 추가 문서

- **[Workflow README](workflow/README.md)** - Snakemake 워크플로우 상세 가이드
- **[Config README](configs/README.md)** - 설정 파일 사용법 및 예시
- **[API Reference](docs/API_REFERENCE.md)** - Python API 문서

### 참조 데이터

필수 참조 파일은 크기 때문에 저장소에 포함되어 있지 않습니다:

- **GO Ontology (OBO):** [Gene Ontology](http://geneontology.org/docs/download-ontology/)에서 다운로드
- **GO Annotations (GAF):** [GOA](http://geneontology.org/docs/download-go-annotations/)에서 다운로드
- **MSigDB Gene Sets:** [MSigDB](https://www.gsea-msigdb.org/gsea/msigdb/)에서 다운로드

참조 파일은 `ref/` 디렉토리에 저장하세요.

### GSEA를 위한 사용자 정의 Gene Set 사용하기

`ref/` 디렉토리에 사용자 정의 gene set을 추가하여 GSEA 분석에 사용할 수 있습니다. Gene set은 **GMT 형식**(Gene Matrix Transposed)이어야 합니다.

#### GMT 형식 구조

GMT 파일은 탭으로 구분된 텍스트 파일로, 각 줄이 하나의 gene set을 나타냅니다:

```
경로명    설명    유전자1    유전자2    유전자3    ...
```

**GMT 파일 예시** (`ref/my_custom_pathways.gmt`):
```
SYNAPSE_GENES    Synaptic_Function_Related    Shank1    Shank2    Shank3    Dlg4    Syngap1
GABA_SIGNALING    GABAergic_Neurotransmission    Gad1    Gad2    Slc32a1    Gabra1    Gabrb2
GLUTAMATE_RECEPTORS    Glutamatergic_Signaling    Grin1    Grin2a    Grin2b    Gria1    Gria2
```

각 줄은 다음을 포함합니다:
1. **Gene set 이름** (예: `SYNAPSE_GENES`)
2. **설명** (예: `Synaptic_Function_Related`)
3. **유전자 심볼** (탭으로 구분, 예: `Shank1    Shank2    Shank3`)

#### Gene Set을 구할 수 있는 곳

**1. MSigDB (Molecular Signatures Database)**
- [MSigDB Downloads](https://www.gsea-msigdb.org/gsea/msigdb/collections.jsp) 방문
- 적절한 컬렉션 선택:
  - **H: Hallmark gene sets** - 잘 정의된 생물학적 상태/프로세스
  - **C2: Curated gene sets** - 온라인 경로 데이터베이스(KEGG, Reactome, BioCarta)
  - **C5: Ontology gene sets** - Gene Ontology 용어
  - **C6: Oncogenic signatures** - 암 관련 시그니처
- 생물종 선택 (Human 또는 Mouse)
- GMT 파일로 다운로드

**2. 문헌에서 사용자 정의 Gene Set 생성**
- 발표된 논문에서 유전자 목록 추출
- 관심 유전자로 자체 GMT 파일 생성
- 기능적 카테고리 또는 경로별로 유전자 그룹화

**3. GO Terms**
- GO annotation을 GMT 형식으로 변환
- 연구와 관련된 특정 GO 용어 사용

**4. 조직/세포 유형 특이적 마커**
- Single-cell RNA-seq 데이터베이스의 마커 유전자 사용
- CellMarker 데이터베이스: [http://xteam.xbio.top/CellMarker/](http://xteam.xbio.top/CellMarker/)
- PanglaoDB: [https://panglaodb.se/](https://panglaodb.se/)

#### 분석에서 사용자 정의 Gene Set 사용하기

**YAML 설정에서** (`workflow/config/gsea_config.yaml`):

```yaml
gsea_analysis:
  mode: prerank  # 또는 "classic"
  
  # 사용자 정의 gene set 파일 사용
  gene_sets:
    - "ref/my_custom_pathways.gmt"
    - "ref/synapse_related_genes.gmt"
  
  # 또는 MSigDB 컬렉션 사용
  # gene_sets:
  #   - "ref/h.all.v2025.1.Mm.symbols.gmt"     # Hallmark
  #   - "ref/c2.cp.kegg.v2025.1.Mm.symbols.gmt"  # KEGG pathways
  
  min_size: 5      # Gene set의 최소 유전자 수
  max_size: 500    # Gene set의 최대 유전자 수
  permutation_num: 1000
```

**예시: 자폐증 관련 사용자 정의 Gene Set 생성**

```bash
# 사용자 정의 GMT 파일 생성
cat > ref/autism_gene_sets.gmt << EOF
ASD_RISK_GENES	Autism_Spectrum_Disorder_Risk_Genes	CHD8	SHANK3	NLGN3	NRXN1	SCN2A	SYNGAP1	PTEN	TSC1	TSC2
SYNAPTIC_ADHESION	Synaptic_Adhesion_Molecules	NLGN1	NLGN2	NLGN3	NLGN4X	NRXN1	NRXN2	NRXN3	LRRTM1	LRRTM2
EXCITATORY_SYNAPSE	Excitatory_Synapse_Proteins	DLG4	GRIN1	GRIN2A	GRIN2B	SHANK1	SHANK2	SHANK3	HOMER1	SYNGAP1
EOF
```

그 다음 분석에서 사용:
```yaml
gsea_analysis:
  gene_sets:
    - "ref/autism_gene_sets.gmt"
```

#### 사용자 정의 Gene Set 모범 사례

1. **유전자 심볼 형식**: 데이터와 일치하는지 확인 (human: 대문자, mouse: 첫글자만 대문자)
2. **크기 제약**: 의미 있는 농축을 위해 gene set을 5-500개 유전자로 유지
3. **문서화**: GMT 파일에 설명적인 이름과 설명 포함
4. **버전 관리**: 분석과 함께 GMT 파일을 버전 관리에 포함
5. **검증**: 전체 분석 실행 전 작은 하위 집합으로 테스트
6. **생물종 호환성**: 생물종에 맞는 gene set 사용 (human vs mouse)

## 🤝 기여

기여를 환영합니다! 이슈를 열거나 Pull Request를 제출해 주세요.

## 📄 라이선스

MIT License - 자세한 내용은 [LICENSE](LICENSE) 파일 참조

---

**English README**: [README_EN.md](README_EN.md)에서 영문 버전을 확인하세요.
