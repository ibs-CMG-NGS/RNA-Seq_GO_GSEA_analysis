# RNA-Seq 후속 분석 파이프라인: GO 및 GSEA

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![English](https://img.shields.io/badge/README-English-blue)](README_EN.md)

RNA-Seq 차등 발현 분석 후 **Gene Ontology (GO) 농축 분석**과 **Gene Set Enrichment Analysis (GSEA)**를 수행하는 모듈화된 Python 파이프라인입니다.

## 🎯 주요 특징

- **🧩 모듈식 설계:** 독립적이고 재사용 가능한 분석 모듈을 자유롭게 조합
- **⚙️ 설정 기반:** YAML 파일로 재현 가능한 분석 수행
- ** Snakemake 통합:** 병렬 처리 및 에러 복구 기능을 갖춘 자동화된 워크플로우
- **📊 논문 수준 결과물:** 고품질 시각화 및 종합 HTML 리포트 생성

## 📋 목차

- [설치](#-설치)
- [빠른 시작](#-빠른-시작)
- [Snakemake 워크플로우](#-snakemake-워크플로우)
- [설정 파일](#-설정)
- [프로젝트 구조](#-프로젝트-구조)
- [라이선스](#-라이선스)

## ✨ 기능

### 분석 기능
- **📥 데이터 로딩 및 표준화:** Excel 파일에서 유연한 컬럼 매핑으로 데이터 로드
- **🔍 유전자 필터링:** 통계적 임계값 또는 커스텀 유전자 리스트로 DEG 추출
- **🧬 GO 농축 분석:** GOATOOLS를 사용한 포괄적인 GO term 농축 분석
- **🎯 GSEA:** Pre-ranked 및 Classic GSEA (MSigDB 또는 커스텀 gene set 지원)
- **📈 시각화:** Volcano plot, GO bar/dot plot, GSEA enrichment plot
- **📄 자동 리포트:** 그래프와 표를 포함한 종합 HTML 리포트

### 워크플로우 기능
- **🔧 모듈식 설계:** 각 분석 단계가 독립적이고 재사용 가능
- ** Snakemake 워크플로우:** 의존성 추적을 통한 자동화된 파이프라인 실행
- **⚡ 병렬 처리:** 다중 코어를 활용한 빠른 배치 분석
- ** 스마트 캐싱:** 입력이 변경될 때만 단계를 재실행

### Prerequisites

## 🚀 설치- Python 3.9 or higher

- Conda package manager (recommended for easy setup)

### 사전 요구사항

- Python 3.9 이상### Recommended Installation with Conda

- Conda 패키지 매니저 (권장)

The easiest way to set up the environment is using the provided `environment.yml` file:

### Conda를 사용한 권장 설치 방법

```bash

제공된 `environment.yml` 파일을 사용하여 환경을 설정하는 것이 가장 쉬운 방법입니다:# 1. Clone the repository

git clone https://github.com/ibs-CMG-NGS/RNA-Seq_GO_GSEA_analysis.git

```bashcd RNA-Seq_GO_GSEA_analysis

# 1. 저장소 복제

git clone https://github.com/ibs-CMG-NGS/RNA-Seq_GO_GSEA_analysis.git# 2. Create and activate conda environment with all dependencies

cd RNA-Seq_GO_GSEA_analysisconda env create -f environment.yml

conda activate rnaseq-analysis

# 2. 모든 의존성이 포함된 conda 환경 생성 및 활성화

conda env create -f environment.yml# 3. (Optional) Install package in development mode for CLI commands

conda activate rnaseq-analysispip install -e .

```

# 3. (선택사항) CLI 명령어 사용을 위해 개발 모드로 패키지 설치

pip install -e .After installation with `-e .`, you can use convenient command aliases:

```- `rnaseq-data-load` instead of `python src/analysis/data_loading.py`

- `rnaseq-filter` instead of `python src/analysis/filtering.py`

`-e .`로 설치하면 편리한 명령어 별칭을 사용할 수 있습니다:- `rnaseq-batch` instead of `python src/analysis/batch_runner.py`

- `rnaseq-data-load` (`python src/analysis/data_loading.py` 대신)- And more! See CLI Reference section for complete list.

- `rnaseq-filter` (`python src/analysis/filtering.py` 대신)

- `rnaseq-batch` (`python src/analysis/batch_runner.py` 대신)### Installation for Snakemake Workflows



### Snakemake 워크플로우용 설치If you want to use Snakemake for workflow automation (recommended for batch processing):



워크플로우 자동화를 위해 Snakemake를 사용하려면 (배치 처리 권장):```bash

# Create Snakemake environment with all dependencies

```bashconda env create -f snakemake_environment.yml

# 모든 의존성이 포함된 Snakemake 환경 생성conda activate snakemake_env

conda env create -f snakemake_environment.yml```

conda activate snakemake_env

```This environment includes Snakemake along with all analysis dependencies.



이 환경에는 Snakemake와 모든 분석 의존성이 포함되어 있습니다.### Alternative Installation (pip + venv)



### 설치 확인If you prefer using pip and virtual environments:



```bash```bash

# 모듈을 import할 수 있는지 테스트# 1. Clone the repository

python -c "import pandas, gseapy, goatools; print('설치 성공!')"git clone https://github.com/ibs-CMG-NGS/RNA-Seq_GO_GSEA_analysis.git

cd RNA-Seq_GO_GSEA_analysis

# CLI 도구 확인

python src/analysis/data_loading.py --help# 2. Create and activate a virtual environment

python -m venv venv

# Snakemake 환경 사용 시 Snakemake 확인source venv/bin/activate  # On Linux/macOS

snakemake --version# OR

```venv\Scripts\activate     # On Windows



## ⚡ 빠른 시작# 3. Install dependencies

pip install -r requirements.txt

### 옵션 1: 인터랙티브 분석 (노트북)

# 4. Install the utility package dependency

단일 샘플 탐색 또는 파이프라인 학습에 적합합니다.pip install git+https://github.com/parkgilbong/YG_utils_analysis.git@main



```bash# 5. (Optional) Install package in development mode for CLI commands

# Jupyter 시작pip install -e .

jupyter notebook```



# 가이드 노트북 중 하나 열기:### Verify Installation

# - notebooks/GO_Pipeline.ipynb (GO 농축 분석용)

# - notebooks/GSEA_Pipeline.ipynb (GSEA 분석용)```bash

```# Test that modules can be imported

python -c "import pandas, gseapy, goatools; print('Installation successful!')"

각 노트북은 다음을 제공합니다:

- 단계별 지침# Check CLI tools

- 인라인 문서python src/analysis/data_loading.py --help

- 인터랙티브 파라미터 조정

- 즉각적인 결과 시각화# If using Snakemake environment, verify Snakemake is available

snakemake --version

### 옵션 2: CLI 단일 분석```



명령줄에서 개별 분석 단계를 실행합니다.## ⚡ Quick Start



```bash### Option 1: Interactive Analysis (Notebooks)

# 방법 A: Python 명령어 직접 사용

python src/analysis/data_loading.py --config configs/GO_pipeline_Shank2.yaml --config-section data_loadingPerfect for exploring a single sample or learning the pipeline.

python src/analysis/filtering.py --config configs/GO_pipeline_Shank2.yaml --config-section filtering

python src/analysis/volcano.py --config configs/GO_pipeline_Shank2.yaml --config-section volcano```bash

python src/analysis/go_enrich.py --config configs/GO_pipeline_Shank2.yaml --config-section go_enrich# Start Jupyter

python src/analysis/report_generation.py --config configs/GO_pipeline_Shank2.yaml --config-section reportjupyter notebook



# 방법 B: 편의 스크립트 사용 (Linux/Mac 권장)# Open one of the guided notebooks:

./scripts/run_go_pipeline.sh configs/GO_pipeline_Shank2.yaml# - notebooks/GO_Pipeline.ipynb (for GO enrichment analysis)

```# - notebooks/GSEA_Pipeline.ipynb (for GSEA analysis)

```

### 옵션 3: Snakemake로 배치 처리 (권장)

Each notebook provides:

**Snakemake**는 복잡한 데이터 분석 파이프라인의 실행을 자동화하는 워크플로우 관리 시스템입니다.- Step-by-step instructions

- Inline documentation

#### Snakemake를 사용하는 이유- Interactive parameter tuning

- Immediate visualization of results

- **🔄 자동 병렬화**: 독립적인 샘플을 자동으로 병렬 실행

- **📊 의존성 추적**: 입력이 변경될 때만 단계를 재실행### Option 2: CLI Single Analysis

- **🔍 재현성**: 내장된 출처 추적 및 워크플로우 문서화

- **⚡ 리소스 관리**: CPU/메모리 리소스의 효율적 할당Run individual analysis steps from the command line.

- **🎯 에러 복구**: 실패 지점에서 다시 시작하지 않고 재개

- **📈 확장성**: 노트북에서 HPC 클러스터까지 원활하게 확장```bash

# Method A: Using direct Python commands

#### 배치 GO 분석 실행python src/analysis/data_loading.py --config configs/GO_pipeline_Shank2.yaml --config-section data_loading

python src/analysis/filtering.py --config configs/GO_pipeline_Shank2.yaml --config-section filtering

```bashpython src/analysis/volcano.py --config configs/GO_pipeline_Shank2.yaml --config-section volcano

# workflow/config/batch_go_config.yaml을 편집하여 샘플 지정python src/analysis/go_enrich.py --config configs/GO_pipeline_Shank2.yaml --config-section go_enrich

# 그런 다음 실행:python src/analysis/report_generation.py --config configs/GO_pipeline_Shank2.yaml --config-section report

snakemake --snakefile workflow/Snakefile_batch_GO \

    --configfile workflow/config/batch_go_config.yaml \# Method B: Using convenience scripts (recommended for Linux/Mac)

    --cores 4./scripts/run_go_pipeline.sh configs/GO_pipeline_Shank2.yaml



# Dry-run (실행될 내용 확인):# Method C: Using installed CLI commands (after 'pip install -e .')

snakemake --snakefile workflow/Snakefile_batch_GO \rnaseq-data-load --config configs/GO_pipeline_Shank2.yaml --config-section data_loading

    --configfile workflow/config/batch_go_config.yaml \rnaseq-filter --config configs/GO_pipeline_Shank2.yaml --config-section filtering

    --dry-runrnaseq-volcano --config configs/GO_pipeline_Shank2.yaml --config-section volcano

```rnaseq-go-enrich --config configs/GO_pipeline_Shank2.yaml --config-section go_enrich

rnaseq-report --config configs/GO_pipeline_Shank2.yaml --config-section report

## 🔗 DE 파이프라인 통합```



이 파이프라인은 [RNA-Seq DE 분석 파이프라인](https://github.com/ibs-CMG-NGS/RNA-Seq_DE_GO_analysis)의 결과를 직접 사용할 수 있도록 설계되었습니다.### Option 3: Batch Processing with Snakemake (Recommended)



### Bridge Layer를 통한 자동 변환**Snakemake** is a workflow management system that automates the execution of complex data analysis pipelines. It provides superior batch processing capabilities compared to sequential Python scripts.



DE 파이프라인의 결과를 GSEA 형식으로 자동 변환하는 bridge layer가 포함되어 있습니다:#### Why Use Snakemake?



```bash- **🔄 Automatic Parallelization**: Run independent samples in parallel automatically

# DE 파이프라인 프로젝트 루트로 이동- **📊 Dependency Tracking**: Only re-run steps when inputs change

cd /path/to/RNA-Seq_DE_GO_analysis- **🔍 Reproducibility**: Built-in provenance tracking and workflow documentation

- **⚡ Resource Management**: Efficient allocation of CPU/memory resources

# Bridge Snakefile 실행 (모든 비교군 자동 변환)- **🎯 Error Recovery**: Resume from where pipeline failed without restarting

snakemake -s bridge/Snakefile --cores 1- **📈 Scalability**: Seamlessly scale from laptop to HPC clusters

- **📉 Visualization**: Generate workflow DAGs for understanding pipeline structure

# 또는 특정 비교만 변환

snakemake -s bridge/Snakefile \#### Setup Snakemake Environment

    data/from_de_pipeline/H2O2_vs_Control_DE_results.xlsx

``````bash

# Create and activate Snakemake environment

**변환되는 내용:**conda env create -f snakemake_environment.yml

- DE 분석 결과 CSV → GSEA 입력 Excel 파일conda activate snakemake_env

- Gene symbol, log2FoldChange, padj 포함```

- **Classic GSEA를 위한 샘플별 expression 데이터 포함** (원본 count matrix가 있는 경우)

#### Run Batch GO Analysis

**출력 위치:**

``````bash

RNA-Seq_GO_GSEA_analysis/data/from_de_pipeline/# Edit workflow/config/batch_go_config.yaml to specify your samples

├── H2O2_vs_Control_DE_results.xlsx# Then run:

├── GABA_vs_Control_DE_results.xlsxsnakemake --snakefile workflow/Snakefile_batch_GO \

└── ...    --configfile workflow/config/batch_go_config.yaml \

```    --cores 4



**💡 팁:** Bridge layer는 Conda 환경을 자동으로 관리하므로 별도 설치가 필요 없습니다.# For dry-run (see what will be executed):

snakemake --snakefile workflow/Snakefile_batch_GO \

자세한 내용은 [DE 파이프라인 README - Bridge Layer 섹션](https://github.com/ibs-CMG-NGS/RNA-Seq_DE_GO_analysis#-bridge-layer-gsea-파이프라인-연결)을 참조하세요.    --configfile workflow/config/batch_go_config.yaml \

    --dry-run

## 📖 사용 가이드```



### 노트북을 통한 인터랙티브 분석#### Run Single Sample Analysis



`notebooks/` 디렉토리에는 인터랙티브 분석을 위한 가이드 Jupyter 노트북이 포함되어 있습니다.```bash

# GO enrichment analysis

#### GO 농축 분석 파이프라인snakemake --snakefile workflow/Snakefile_GO \

    --configfile workflow/config/go_config.yaml \

**노트북:** `GO_Pipeline.ipynb`    --cores 1



**파이프라인 단계:**# GSEA analysis

1. **데이터 로딩** (`data_loading.py`) - Excel 입력 파일 표준화snakemake --snakefile workflow/Snakefile_GSEA \

2. **필터링** (`filtering.py`) - 유의미한 DEG 추출    --configfile workflow/config/gsea_config.yaml \

3. **Volcano Plot** (`volcano.py`) - 차등 발현 시각화    --cores 1

4. **GO 농축** (`go_enrich.py`) - 농축된 GO term 식별```

5. **GO 시각화** (`go_barplot.py`) - Bar/dot plot 생성

6. **리포트 생성** (`report_generation.py`) - HTML 리포트 컴파일#### Visualize Workflow



**설정:** `configs/GO_pipeline_*.yaml` 파일 편집```bash

# Generate workflow diagram (requires graphviz)

#### GSEA 분석 파이프라인snakemake --snakefile workflow/Snakefile_GO \

    --configfile workflow/config/go_config.yaml \

**노트북:** `GSEA_Pipeline.ipynb`    --dag | dot -Tpng > workflow_dag.png

```

**파이프라인 단계:**

1. **데이터 로딩** (`data_loading.py`) - Ranked gene list 또는 expression matrix 준비#### HPC/Cluster Execution

2. **GSEA 분석** (`gsea_analysis.py`) - Pre-ranked 또는 Classic GSEA 실행

3. **GSEA 시각화** (`gsea_plot.py`) - Enrichment plot 생성For SLURM clusters:



**설정:** `configs/GSEA_pipeline.yaml` 편집```bash

snakemake --snakefile workflow/Snakefile_batch_GO \

### 🎯 GSEA 분석 모드    --configfile workflow/config/batch_go_config.yaml \

    --cluster "sbatch --time=02:00:00 --mem=16G --cpus-per-task=1" \

GSEA는 두 가지 모드를 지원하며, 각각 다른 입력 데이터 형식을 요구합니다.    --jobs 10

```

#### 1. Pre-ranked GSEA (권장)

The Snakemake approach will:

**사용 시기:**- Process samples in parallel when resources allow

- ✅ DE 분석 결과가 있을 때- Automatically manage dependencies between analysis steps

- ✅ 빠른 분석이 필요할 때- Resume from failure points without re-running completed steps

- ✅ 샘플 수가 적을 때- Generate detailed logs for each rule execution

- Create organized output directories per sample

**필요한 입력:**- Track which files were generated and when

- Gene symbol과 ranking metric (예: log2FoldChange)이 포함된 표

See the [Workflow README](workflow/README.md) for detailed Snakemake usage instructions.

**장점:**

- ⚡ 빠른 실행 속도### Option 4: Batch Processing with Python (Alternative)

- 💾 적은 메모리 사용

- 🔢 샘플 수에 무관For users who prefer Python-based batch processing or don't have Snakemake:

- ✅ 안정적이고 검증된 방법

```bash

**설정 예시:**# Method A: Direct Python command

```yamlpython src/analysis/batch_runner.py --manifest configs/batch_manifest_H2O2.yaml

# configs/gsea_config.yaml

gsea:# Method B: Using installed CLI (after 'pip install -e .')

  mode: prerank  # Pre-ranked 모드rnaseq-batch --manifest configs/batch_manifest_H2O2.yaml

  ```

  # Pre-ranked 모드 설정

  prerank_input_csv: "standardized.csv"The Python batch runner will:

  rank_metric_column: "log2FoldChange"- Process each sample sequentially

  gene_symbol_column: "symbol"- Generate sample-specific output directories

  - Create temporary configurations per sample

  # Gene sets- Log progress and errors for debugging

  gene_sets:

    - "GO_Biological_Process_2023"**Note**: While the Python batch runner is simpler, Snakemake offers better performance, 

    - "GO_Molecular_Function_2023"error recovery, and scalability for processing multiple samples.

    - "ref/custom_pathways.gmt"

```### Helper Scripts



**실행:**The `scripts/` directory contains convenient wrapper scripts:

```bash

# Data loading으로 ranked list 준비```bash

python src/analysis/data_loading.py \# Run complete GO pipeline

    --config configs/gsea_config.yaml \./scripts/run_go_pipeline.sh configs/GO_pipeline_Shank2.yaml

    --config-section data_loading

# Run complete GSEA pipeline

# Pre-ranked GSEA 실행./scripts/run_gsea_pipeline.sh configs/GSEA_pipeline.yaml

python src/analysis/gsea_analysis.py \```

    --config configs/gsea_config.yaml \

    --config-section gseaThese scripts:

```- Run all pipeline steps automatically

- Show progress for each step

#### 2. Classic GSEA- Exit immediately if any step fails

- Work on Linux, macOS, and Windows (via Git Bash/WSL)

**사용 시기:**

- 📊 전체 expression matrix가 있을 때## 📖 Usage Guide

- 🔬 샘플별 발현 패턴을 분석하고 싶을 때

- 🎯 순열 검정(permutation test)을 통한 엄격한 통계 검정이 필요할 때### Interactive Analysis with Notebooks



**필요한 입력:**The `notebooks/` directory contains guided Jupyter notebooks for interactive analysis.

1. **Expression matrix** (유전자 × 샘플)

2. **Class labels file** (샘플의 그룹 정보)#### GO Enrichment Analysis Pipeline



**장점:****Notebook:** `GO_Pipeline.ipynb`

- 📈 샘플 간 변동성 고려

- 🎲 더 엄격한 통계 검정**Pipeline Stages:**

- 📚 표준 GSEA 방법론1. **Data Loading** (`data_loading.py`) - Standardize Excel input files

2. **Filtering** (`filtering.py`) - Extract significant DEGs

**단점:**3. **Volcano Plot** (`volcano.py`) - Visualize differential expression

- ⏱️ 느린 실행 속도4. **GO Enrichment** (`go_enrich.py`) - Identify enriched GO terms

- 💻 많은 메모리 필요5. **GO Visualization** (`go_barplot.py`) - Create bar/dot plots

- 👥 충분한 샘플 수 필요 (그룹당 3개 이상 권장)6. **Report Generation** (`report_generation.py`) - Compile HTML report



**데이터 준비:****Configuration:** Edit `configs/GO_pipeline_*.yaml` files



Classic GSEA는 다음 두 파일이 필요합니다:#### GSEA Analysis Pipeline



1. **Expression Matrix** (`gsea_expression_matrix.txt`):**Notebook:** `GSEA_Pipeline.ipynb`

```

NAME          DESCRIPTION  Sample1  Sample2  Sample3  Sample4**Pipeline Stages:**

Ptx3          Ptx3         664.31   958.34   1094.85  1776.331. **Data Loading** (`data_loading.py`) - Prepare ranked gene lists or expression matrix

Gpnmb         Gpnmb        288.93   417.31   387.45   596.862. **GSEA Analysis** (`gsea_analysis.py`) - Run pre-ranked or classic GSEA

Tuba4a        Tuba4a       9298.09  9291.95  9112.01  6941.393. **GSEA Visualization** (`gsea_plot.py`) - Generate enrichment plots

```

**Configuration:** Edit `configs/GSEA_pipeline.yaml`

2. **Class Labels File** (`gsea_class_labels.cls`):

```### Command-Line Analysis

4 2 1

# Control TreatmentEach module accepts both CLI arguments and YAML configuration. CLI arguments override config file values.

0 0 1 1

```**Example: Running filtering with CLI overrides**

- 첫 줄: 샘플 수, 그룹 수, 1 (categorical)

- 둘째 줄: 그룹 이름```bash

- 셋째 줄: 각 샘플의 그룹 (0-indexed numeric labels)python src/analysis/filtering.py \

  --config configs/GO_pipeline_Shank2.yaml \

**설정 예시:**  --config-section filtering \

```yaml  --padj-cutoff 0.01 \

# configs/gsea_config.yaml  --log2fc-cutoff 1.5 \

data_loading:  --direction up

  # Excel 파일에 샘플별 expression 데이터가 있어야 함```

  gsea_outputs:

    enabled: true### Batch Processing

    expression_matrix_file: "gsea_expression_matrix.txt"

    class_labels_file: "gsea_class_labels.cls"Create a manifest file defining your batch analysis:

    sample_columns:

      Treatment: ["H2O2_3", "H2O2_6", "H2O2_7"]```yaml

      Control: ["Ctrl_3", "Ctrl_4", "Ctrl_8"]# configs/my_batch_manifest.yaml

base_config_path: "configs/GO_pipeline_template.yaml"

gsea:output_root: "results/my_batch_{timestamp}"

  mode: classic  # Classic GSEA 모드

  pipeline_steps:

  # Classic 모드 설정  - data_loading

  expression_matrix_csv: "gsea_expression_matrix.txt"  - filtering

  class_labels_file: "gsea_class_labels.cls"  - volcano

    - go_enrich

  # Gene sets  - go_barplot

  gene_sets:  - report_generation

    - "GO_Biological_Process_2023"

    - "ref/m5.go.v2025.1.Mm.symbols.gmt"samples:

```  - name: "sample1"

    overrides:

**실행:**      data_loading:

```bash        excel_path: "data/sample1.xlsx"

# 1. Expression matrix와 class labels 생성  - name: "sample2"

python src/analysis/data_loading.py \    overrides:

    --config configs/gsea_config.yaml \      data_loading:

    --config-section data_loading        excel_path: "data/sample2.xlsx"

```

# 2. Classic GSEA 실행

python src/analysis/gsea_analysis.py \Execute:

    --config configs/gsea_config.yaml \```bash

    --config-section gseapython src/analysis/batch_runner.py --manifest configs/my_batch_manifest.yaml

``````



#### 모드 선택 가이드## 🐍 Snakemake Workflow Automation



| 기준 | Pre-ranked | Classic |Snakemake is a powerful workflow management system that brings reproducibility, scalability, and efficiency to your RNA-Seq analysis. This section provides comprehensive guidance on using Snakemake workflows.

|------|-----------|---------|

| **샘플 수** | 무관 | 그룹당 3개 이상 권장 |### Why Snakemake?

| **실행 속도** | 빠름 (분) | 느림 (시간) |

| **메모리** | 적음 | 많음 |Snakemake offers significant advantages over traditional sequential batch processing:

| **입력 데이터** | Ranked list | Expression matrix |

| **통계 엄격성** | 보통 | 높음 |#### Key Benefits

| **추천 용도** | 일반적인 DE 후속 분석 | 샘플이 충분할 때 |

1. **Automatic Parallelization**

**💡 권장사항:**   - Executes independent samples and steps in parallel

- 대부분의 경우 **Pre-ranked 모드** 사용   - Maximizes resource utilization on multi-core systems

- 샘플이 충분하고(그룹당 5개 이상) 더 엄격한 분석이 필요하면 **Classic 모드** 사용   - Reduces total analysis time by 3-5x for batch processing

- DE 파이프라인에서 변환된 데이터는 **두 모드 모두 지원**

2. **Smart Dependency Management**

## 🐍 Snakemake 워크플로우   - Tracks input/output relationships automatically

   - Only re-runs steps when inputs change

Snakemake는 RNA-Seq 분석에 재현성, 확장성, 효율성을 제공하는 강력한 워크플로우 관리 시스템입니다.   - Avoids redundant computations



### 기본 사용법3. **Reproducibility**

   - Built-in provenance tracking

#### 단일 샘플 분석   - Version-controlled workflow definitions

   - Documented execution history

```bash

# GO 농축 분석4. **Error Recovery**

snakemake --snakefile workflow/Snakefile_GO \   - Resume from failure points without restarting

    --configfile configs/go_config.yaml \   - No need to re-run successful steps

    --cores 1   - Save time and computational resources



# GSEA 분석5. **Scalability**

snakemake --snakefile workflow/Snakefile_GSEA \   - Seamlessly scale from laptop to HPC clusters

    --configfile configs/gsea_config.yaml \   - Works with SLURM, PBS, LSF, and other schedulers

    --cores 1   - Cloud execution support (AWS, Google Cloud)

```

6. **Visualization**

#### 워크플로우 시각화   - Generate workflow DAGs

   - Understand pipeline structure at a glance

```bash   - Debug complex workflows easily

# 워크플로우 다이어그램 생성 (graphviz 필요)

snakemake --snakefile workflow/Snakefile_GO \### Workflow Types

    --configfile configs/go_config.yaml \

    --dag | dot -Tpng > workflow_dag.pngWe provide three Snakemake workflows:

```

1. **`Snakefile_GO`** - Single-sample GO enrichment analysis

### ⚡ 배치 GSEA 워크플로우2. **`Snakefile_GSEA`** - Single-sample GSEA analysis

3. **`Snakefile_batch_GO`** - Multi-sample batch GO analysis

여러 샘플의 GSEA 분석을 자동화하고 병렬 처리하는 Snakemake 워크플로우입니다.

### Quick Start with Snakemake

#### 1. 설정 파일 준비

#### 1. Setup Environment

`workflow/config/batch_gsea_config.yaml` 파일을 생성하거나 편집:

```bash

```yaml# Create and activate Snakemake environment

# 배치 분석 결과를 저장할 루트 디렉토리conda env create -f snakemake_environment.yml

output_root: "results/batch_gsea_H2O2_GABA"conda activate snakemake_env

```

# 분석할 샘플 목록

samples:#### 2. Configure Your Analysis

  - name: "H2O2-treated"

    overrides:Edit the workflow configuration file for your analysis type:

      data_loading:

        excel_path: "data/from_de_pipeline/H2O2_vs_Control_DE_results.xlsx"```bash

        sheets: "DE_Results"# For single GO analysis

        # Classic GSEA를 위한 샘플 컬럼 지정 (expression 데이터가 있는 경우)nano workflow/config/go_config.yaml

        gsea_outputs:

          enabled: true# For batch GO analysis

          sample_columns:nano workflow/config/batch_go_config.yaml

            H2O2: ["H2O2_3", "H2O2_6", "H2O2_7"]```

            Ctrl: ["Ctrl_3", "Ctrl_4", "Ctrl_8"]

#### 3. Dry Run (Preview)

  - name: "GABA-treated"

    overrides:Always preview what will be executed:

      data_loading:

        excel_path: "data/from_de_pipeline/GABA_vs_Control_DE_results.xlsx"```bash

        sheets: "DE_Results"# Single sample GO analysis

        gsea_outputs:snakemake --snakefile workflow/Snakefile_GO \

          enabled: true    --configfile workflow/config/go_config.yaml \

          sample_columns:    --dry-run --printshellcmds

            GABA: ["GABA_5", "GABA_6", "GABA_8"]

            Ctrl: ["Ctrl_3", "Ctrl_4", "Ctrl_8"]# Batch GO analysis

snakemake --snakefile workflow/Snakefile_batch_GO \

# 모든 샘플에 공통으로 적용되는 기본 설정    --configfile workflow/config/batch_go_config.yaml \

base_config:    --dry-run --printshellcmds

  data_loading:```

    gene_col: "symbol"

    log2fc_col: "log2FoldChange"#### 4. Execute Workflow

    padj_col: "padj"

    csv_file: "standardized.csv"```bash

    # Single sample (1 core)

  gsea:snakemake --snakefile workflow/Snakefile_GO \

    # 분석 모드: "prerank" 또는 "classic"    --configfile workflow/config/go_config.yaml \

    mode: classic  # Classic GSEA 사용    --cores 1

    

    # GSEA 파라미터# Batch processing (4 cores for parallel execution)

    min_size: 15snakemake --snakefile workflow/Snakefile_batch_GO \

    max_size: 500    --configfile workflow/config/batch_go_config.yaml \

    permutation_num: 5000    --cores 4

    seed: 42```

    

    # 분석할 gene set 목록### Advanced Snakemake Usage

    gene_sets:

      - "GO_Biological_Process_2023"#### Workflow Visualization

      - "GO_Molecular_Function_2023"

      - "GO_Cellular_Component_2023"Generate visual representations of your workflow:

      - "MSigDB_Hallmark_2020"

      - "ref/mh.all.v2025.1.Mm.symbols.gmt"```bash

      - "ref/m5.go.v2025.1.Mm.symbols.gmt"# DAG (Directed Acyclic Graph) showing all jobs

    snakemake --snakefile workflow/Snakefile_GO \

    gsea_output_dir: "gsea_results"    --configfile workflow/config/go_config.yaml \

    output_excel_file: "GSEA_Report.xlsx"    --dag | dot -Tpng > workflow_dag.png

  

  gsea_plot:# Rule graph showing workflow structure

    fdr_cutoff: 0.25snakemake --snakefile workflow/Snakefile_GO \

    top_n_plots: 15    --configfile workflow/config/go_config.yaml \

    plot_formats:    --rulegraph | dot -Tpng > workflow_rules.png

      - "png"

      - "svg"# File graph showing input/output dependencies

```snakemake --snakefile workflow/Snakefile_GO \

    --configfile workflow/config/go_config.yaml \

#### 2. 워크플로우 실행    --filegraph | dot -Tpng > workflow_files.png

```

```bash

# Snakemake 환경 활성화#### Executing Specific Rules

conda activate snakemake_env

Run only certain steps of the pipeline:

# Dry-run으로 실행 계획 확인

snakemake -s workflow/Snakefile_batch_GSEA \```bash

    --configfile workflow/config/batch_gsea_config.yaml \# Run only data loading and filtering

    --dry-runsnakemake --snakefile workflow/Snakefile_GO \

    --configfile workflow/config/go_config.yaml \

# 실제 실행 (2개 코어 사용, 샘플 병렬 처리)    --until filtering --cores 1

snakemake -s workflow/Snakefile_batch_GSEA \

    --configfile workflow/config/batch_gsea_config.yaml \# Run only the GO enrichment step

    --cores 2snakemake --snakefile workflow/Snakefile_GO \

```    --configfile workflow/config/go_config.yaml \

    --forcerun go_enrich --cores 1

#### 3. 출력 구조```



```#### Force Re-execution

results/batch_gsea_H2O2_GABA/

├── H2O2-treated/Force re-running of specific steps or entire workflow:

│   ├── GSEA_Report.xlsx                    # 통합 결과 리포트 ⭐

│   ├── standardized.csv                    # 표준화된 입력 데이터```bash

│   ├── gsea_expression_matrix.txt          # Classic GSEA용 expression matrix# Re-run entire workflow

│   ├── gsea_class_labels.cls               # Classic GSEA용 class labelssnakemake --snakefile workflow/Snakefile_GO \

│   ├── plots/                              # 시각화 결과 ⭐    --configfile workflow/config/go_config.yaml \

│   │   ├── dotplot_GO_Biological_Process_2023.png    --forceall --cores 1

│   │   ├── barplot_GO_Molecular_Function_2023.png

│   │   ├── dotplot_MSigDB_Hallmark_2020.png# Re-run from a specific rule onwards

│   │   └── ...snakemake --snakefile workflow/Snakefile_GO \

│   ├── GSEA_Report/                        # 상세 GSEA 결과    --configfile workflow/config/go_config.yaml \

│   │   ├── GO_Biological_Process_2023/    --forcerun go_enrich --cores 1

│   │   │   ├── gseapy.phenotype.gsea.report.csv```

│   │   │   └── gsea/

│   │   ├── MSigDB_Hallmark_2020/#### Cluster/HPC Execution

│   │   └── ...

│   └── logs/##### SLURM Clusters

│       ├── data_loading.log

│       ├── gsea_analysis.log```bash

│       └── gsea_plot.log# Basic SLURM submission

│snakemake --snakefile workflow/Snakefile_batch_GO \

└── GABA-treated/    --configfile workflow/config/batch_go_config.yaml \

    ├── GSEA_Report.xlsx    --cluster "sbatch --time=02:00:00 --mem=16G --cpus-per-task=1" \

    ├── plots/    --jobs 10

    └── ...

```# With custom resource allocation per rule

snakemake --snakefile workflow/Snakefile_batch_GO \

#### 4. 주요 출력 파일    --configfile workflow/config/batch_go_config.yaml \

    --cluster "sbatch --time={resources.time} --mem={resources.mem_mb}M" \

**`GSEA_Report.xlsx`** - 모든 gene set 분석 결과가 통합된 Excel 파일:    --default-resources time=60 mem_mb=8000 \

- 각 gene set이 별도 시트로 저장    --jobs 20

- 컬럼: Term, ES, NES, p-value, FDR q-value, Gene ratio 등```

- 바로 논문이나 발표에 사용 가능

##### PBS/Torque Clusters

**`plots/`** - 유의미한 결과에 대한 시각화:

- **Dotplot**: 농축 점수와 유의성을 점으로 표현```bash

- **Barplot**: 상위 pathway를 막대 그래프로 표현snakemake --snakefile workflow/Snakefile_batch_GO \

- FDR < 0.25 기준을 만족하는 결과만 플롯 생성    --configfile workflow/config/batch_go_config.yaml \

    --cluster "qsub -l walltime=02:00:00 -l mem=16gb" \

#### 5. 고급 사용법    --jobs 10

```

**특정 샘플만 실행:**

```bash#### Monitoring and Logging

# H2O2-treated 샘플만 분석

snakemake -s workflow/Snakefile_batch_GSEA \```bash

    --configfile workflow/config/batch_gsea_config.yaml \# Detailed progress logging

    results/batch_gsea_H2O2_GABA/H2O2-treated/GSEA_Report.xlsx \snakemake --snakefile workflow/Snakefile_batch_GO \

    --cores 1    --configfile workflow/config/batch_go_config.yaml \

```    --cores 4 \

    --printshellcmds \

**특정 단계만 재실행:**    --verbose

```bash

# 플롯만 다시 생성 (FDR cutoff 변경 후)# Save logs to file

snakemake -s workflow/Snakefile_batch_GSEA \snakemake --snakefile workflow/Snakefile_batch_GO \

    --configfile workflow/config/batch_gsea_config.yaml \    --configfile workflow/config/batch_go_config.yaml \

    --forcerun gsea_plot \    --cores 4 \

    --cores 2    2>&1 | tee snakemake_run.log

``````



**HPC 클러스터에서 실행 (SLURM):**### Batch Configuration Example

```bash

snakemake -s workflow/Snakefile_batch_GSEA \Here's a complete example of `workflow/config/batch_go_config.yaml`:

    --configfile workflow/config/batch_gsea_config.yaml \

    --cluster "sbatch --time=02:00:00 --mem=16G --cpus-per-task=1" \```yaml

    --jobs 10# Output directory for all samples

```output_root: "results/batch_go_snakemake"



#### 6. Prerank vs Classic 선택# Base configuration applied to all samples

base_config:

배치 GSEA에서 모드를 변경하려면 `base_config.gsea.mode` 설정:  filtering:

    mode: thresholds

**Prerank 모드로 변경:**    padj_cutoff: 0.05

```yaml    log2fc_cutoff: 0

base_config:    direction: both

  data_loading:  

    gsea_outputs:  go_enrich:

      enabled: false  # Expression matrix 생성 안 함    obo: "ref/go-basic.obo"

      gaf: "ref/goa_mouse.gaf"

  gsea:    taxon: 10090

    mode: prerank  # Pre-ranked GSEA    alpha: 0.05

```

# Sample definitions

**Classic 모드 (기본):**samples:

```yaml  - name: "Control_vs_Treatment1"

base_config:    overrides:

  data_loading:      data_loading:

    gsea_outputs:        excel_path: "data/exp1.xlsx"

      enabled: true  # Expression matrix 생성        sheets: "Sheet1"

      # sample_columns은 각 샘플의 overrides에서 지정        gene_col: "Gene Symbol"

          log2fc_col: "log2FC"

  gsea:        padj_col: "padj"

    mode: classic  # Classic GSEA      report:

```        title: "GO Analysis: Control vs Treatment1"

        sample_name: "Treatment1"

**💡 팁:**  

- Classic 모드 사용 시 각 샘플의 `sample_columns`를 정확히 지정해야 합니다  - name: "Control_vs_Treatment2"

- Gene names가 정수로 변환되는 문제는 파이프라인에서 자동으로 처리됩니다    overrides:

- Class labels는 numeric format (0, 1)으로 자동 생성됩니다      data_loading:

        excel_path: "data/exp2.xlsx"

### HPC/클러스터 실행        sheets: "Sheet1"

      filtering:

SLURM 클러스터의 경우:        padj_cutoff: 0.01  # Stricter threshold for this sample

      report:

```bash        title: "GO Analysis: Control vs Treatment2"

snakemake --snakefile workflow/Snakefile_batch_GO \        sample_name: "Treatment2"

    --configfile workflow/config/batch_go_config.yaml \```

    --cluster "sbatch --time=02:00:00 --mem=16G --cpus-per-task=1" \

    --jobs 10### Troubleshooting

```

#### Common Issues

자세한 Snakemake 사용법은 [Workflow README](workflow/README.md)를 참조하세요.

**Issue**: "MissingInputException: Missing input files"

## ⚙️ 설정```bash

# Solution: Check if input files exist and paths are correct

모든 분석 파라미터는 YAML 파일로 관리됩니다. `configs/` 디렉토리에 다양한 템플릿이 있습니다:snakemake --snakefile workflow/Snakefile_GO \

    --configfile workflow/config/go_config.yaml \

- `GO_pipeline_*.yaml` - GO 농축 분석 설정    --dry-run --verbose

- `GSEA_pipeline.yaml` - GSEA 분석 설정```

- `batch_manifest_*.yaml` - 배치 처리 매니페스트

- `batch_go_config.yaml` - 배치 GO 분석 Snakemake 설정**Issue**: "AmbiguousRuleException"

- `batch_gsea_config.yaml` - 배치 GSEA 분석 Snakemake 설정```bash

# Solution: Be more specific with target files or rules

각 설정 파일에는 상세한 주석이 포함되어 있어 파라미터를 쉽게 이해하고 수정할 수 있습니다.snakemake --snakefile workflow/Snakefile_GO \

    --configfile workflow/config/go_config.yaml \

## 📁 프로젝트 구조    --until rule_name --cores 1

```

```

RNA-Seq_GO_GSEA_analysis/**Issue**: Jobs fail but Snakemake doesn't show errors

├── configs/                      # YAML 설정 파일```bash

│   ├── GO_pipeline_*.yaml# Solution: Check log files in output directory

│   ├── GSEA_pipeline.yamlcat results/batch_go_snakemake/sample1/logs/*.log

│   ├── batch_go_config.yaml```

│   └── batch_gsea_config.yaml

├── data/                         # 입력 데이터### Performance Optimization

│   ├── from_de_pipeline/         # DE 파이프라인 결과

│   └── processed/For optimal performance when processing multiple samples:

├── notebooks/                    # Jupyter 노트북

│   ├── GO_Pipeline.ipynb```bash

│   └── GSEA_Pipeline.ipynb# Use appropriate core count (typically: number of samples or CPU cores)

├── src/                          # 소스 코드# Example: 8 samples on a 16-core machine

│   └── analysis/snakemake --snakefile workflow/Snakefile_batch_GO \

│       ├── data_loading.py    --configfile workflow/config/batch_go_config.yaml \

│       ├── filtering.py    --cores 8

│       ├── gsea_analysis.py

│       └── ...# For cluster execution, match jobs to available nodes

├── workflow/                     # Snakemake 워크플로우# Example: 50 samples on cluster with 10 available nodes

│   ├── Snakefile_GOsnakemake --snakefile workflow/Snakefile_batch_GO \

│   ├── Snakefile_GSEA    --configfile workflow/config/batch_go_config.yaml \

│   ├── Snakefile_batch_GO    --cluster "sbatch --time=02:00:00 --mem=16G" \

│   ├── Snakefile_batch_GSEA    --jobs 10

│   └── config/```

├── scripts/                      # 헬퍼 스크립트

│   ├── run_go_pipeline.sh### Best Practices

│   └── run_gsea_pipeline.sh

├── ref/                          # 참조 파일 (GMT 등)1. **Always dry-run first**: Use `--dry-run` to preview execution

├── results/                      # 분석 결과 (자동 생성)2. **Use version control**: Commit workflow and config files to git

├── debug/                        # 디버깅 스크립트3. **Document parameters**: Add comments to configuration files

├── environment.yml               # Conda 환경 설정4. **Check logs**: Review execution logs for errors and warnings

├── snakemake_environment.yml     # Snakemake 환경 설정5. **Visualize workflows**: Generate DAGs to understand pipeline structure

├── README.md                     # 한국어 README (이 파일)6. **Start small**: Test with 1-2 samples before full batch processing

└── README_EN.md                  # 영문 README7. **Monitor resources**: Track memory and CPU usage during execution

```8. **Use appropriate cores**: Match `--cores` to your system capabilities



## 🤝 기여### Additional Resources



기여를 환영합니다! 이슈를 열거나 Pull Request를 제출해 주세요.- **Workflow README**: See `workflow/README.md` for detailed workflow documentation

- **Snakemake Documentation**: https://snakemake.readthedocs.io/

## 📞 지원- **Tutorial**: https://snakemake.readthedocs.io/en/stable/tutorial/tutorial.html

- **Best Practices**: https://snakemake.readthedocs.io/en/stable/snakefiles/best_practices.html

질문이나 문제가 있으시면:

- GitHub Issues 열기## ⚙️ Configuration

- 개발팀에 문의

The pipeline uses YAML configuration files for all parameters. This design enables:

## 📄 라이선스- **Reproducibility:** Same config = same results

- **Version Control:** Track parameter changes in git

MIT License - 자세한 내용은 [LICENSE](LICENSE) 파일 참조- **Documentation:** Self-documenting analysis parameters



---### Configuration Types



**English README**: [README_EN.md](README_EN.md)에서 영문 버전을 확인하세요.#### 1. Pipeline Configuration Files


Located in `configs/`, these define all parameters for a complete analysis.

**Structure:**
```yaml
ROOT_DIR: "output/my_analysis"  # Base output directory

data_loading:
  excel_path: "data/input.xlsx"
  sheets: "Sheet1"
  gene_col: "Gene Symbol"
  log2fc_col: "log2FoldChange"
  padj_col: "padj"
  csv_file: "standardized.csv"

filtering:
  in_csv_file: "standardized.csv"
  mode: thresholds
  padj_cutoff: 0.05
  log2fc_cutoff: 1.0
  direction: both
  out_csv_file: "filtered.csv"

volcano:
  in_csv_file: "standardized.csv"
  out_png_file: "volcano.png"
  padj_cutoff: 0.05
  log2fc_cutoff: 1.0

go_enrich:
  filtered_csv: "filtered.csv"
  background_csv: "standardized.csv"
  obo: "ref/go-basic.obo"
  gaf: "ref/goa_human.gaf"
  alpha: 0.05
  goea_csv_file: "go_results.csv"
```

**Examples:**
- `GO_pipeline_Shank2.yaml` - Complete GO analysis config
- `GO_pipeline_H2O2.yaml` - H2O2 treatment analysis
- `GSEA_pipeline.yaml` - GSEA analysis config

#### 2. Batch Manifest Files

Define multi-sample batch processing workflows.

**Structure:**
```yaml
base_config_path: "configs/GO_pipeline_template.yaml"
output_root: "results/batch_{timestamp}"

pipeline_steps:
  - data_loading
  - filtering
  - volcano
  - go_enrich
  - report_generation

samples:
  - name: "control_vs_treatment1"
    overrides:
      data_loading:
        excel_path: "data/treatment1.xlsx"
        sheets: "DEG_results"
      
  - name: "control_vs_treatment2"
    overrides:
      data_loading:
        excel_path: "data/treatment2.xlsx"
      filtering:
        padj_cutoff: 0.01  # Stricter threshold
```

**Features:**
- **Base Config:** Shared parameters across all samples
- **Sample Overrides:** Customize per-sample settings
- **Pipeline Steps:** Choose which steps to run
- **Output Organization:** Automatic timestamped directories

### Configuration Best Practices

1. **Use Templates:** Start from example configs and modify
2. **Relative Paths:** Use paths relative to project root
3. **Version Control:** Commit configs alongside code
4. **Document Changes:** Add comments for non-obvious parameters
5. **Test First:** Validate configs on small datasets

## 🖥️ CLI Reference

All analysis modules support a consistent CLI interface with three usage methods:

```bash
# Method 1: Direct Python module execution
python src/analysis/<module>.py --config <config.yaml> --config-section <section>

# Method 2: Installed CLI commands (after 'pip install -e .')
rnaseq-<command> --config <config.yaml> --config-section <section>

# Method 3: Helper scripts
./scripts/run_go_pipeline.sh <config.yaml>
```

### Core Analysis Modules

| Python Module | CLI Command | Purpose | Key Parameters |
|---------------|-------------|---------|----------------|
| `data_loading.py` | `rnaseq-data-load` | Load and standardize input data | `--excels`, `--sheets`, `--gene-col` |
| `filtering.py` | `rnaseq-filter` | Filter DEGs by thresholds | `--padj-cutoff`, `--log2fc-cutoff`, `--direction` |
| `volcano.py` | `rnaseq-volcano` | Generate volcano plots | `--padj-cutoff`, `--log2fc-cutoff`, `--xlim`, `--ylim` |
| `go_enrich.py` | `rnaseq-go-enrich` | Run GO enrichment | `--genes-file`, `--background-csv`, `--obo`, `--gaf` |
| `go_barplot.py` | `rnaseq-go-barplot` | Visualize GO results | `--in-csv`, `--out-png`, `--top-terms` |
| `gsea_analysis.py` | `rnaseq-gsea` | Run GSEA | `--mode`, `--gene-sets`, `--min-size`, `--max-size` |
| `gsea_plot.py` | `rnaseq-gsea-plot` | Visualize GSEA results | `--results-dir`, `--top-terms` |
| `report_generation.py` | `rnaseq-report` | Generate HTML report | All previous outputs |
| `batch_runner.py` | `rnaseq-batch` | Batch processing | `--manifest` |

### Common CLI Patterns

**Get help for any module:**
```bash
python src/analysis/filtering.py --help
```

**Override config with CLI arguments:**
```bash
python src/analysis/filtering.py \
  --config configs/pipeline.yaml \
  --config-section filtering \
  --padj-cutoff 0.01 \
  --log2fc-cutoff 2.0
```

**Use without config file (all CLI args):**
```bash
python src/analysis/volcano.py \
  --in-csv output/standardized.csv \
  --out-png output/volcano.png \
  --padj-cutoff 0.05 \
  --log2fc-cutoff 1.0
```

### Linux/HPC Usage Examples

**Submit to SLURM:**
```bash
#!/bin/bash
#SBATCH --job-name=rnaseq_batch
#SBATCH --time=4:00:00
#SBATCH --mem=16G

module load python/3.9
source venv/bin/activate

python src/analysis/batch_runner.py \
  --manifest configs/batch_manifest.yaml
```

**Run in background with logging:**
```bash
nohup python src/analysis/batch_runner.py \
  --manifest configs/batch_manifest.yaml \
  > batch_analysis.log 2>&1 &
```

**Chain commands in bash script:**
```bash
#!/bin/bash
set -e  # Exit on error

CONFIG="configs/GO_pipeline.yaml"

python src/analysis/data_loading.py --config $CONFIG --config-section data_loading
python src/analysis/filtering.py --config $CONFIG --config-section filtering
python src/analysis/volcano.py --config $CONFIG --config-section volcano
python src/analysis/go_enrich.py --config $CONFIG --config-section go_enrich
python src/analysis/report_generation.py --config $CONFIG --config-section report

echo "Pipeline complete!"
```

## 📁 Project Structure

```
RNA-Seq_GO_GSEA_analysis/
│
├── scripts/                      # Convenience wrapper scripts
│   ├── run_go_pipeline.sh       # Run complete GO pipeline
│   └── run_gsea_pipeline.sh     # Run complete GSEA pipeline
│
├── configs/                      # Configuration files
│   ├── GO_pipeline_*.yaml       # GO analysis configurations
│   ├── GSEA_pipeline.yaml       # GSEA configuration
│   ├── batch_manifest_*.yaml    # Batch processing manifests (for Python batch_runner)
│   └── genes_of_interest.txt    # Example gene lists
│
├── workflow/                     # Snakemake workflow files
│   ├── Snakefile_GO             # GO analysis workflow
│   ├── Snakefile_GSEA           # GSEA analysis workflow
│   ├── Snakefile_batch_GO       # Batch GO analysis workflow
│   ├── README.md                # Workflow usage documentation
│   ├── config/                  # Workflow configurations
│   │   ├── go_config.yaml       # GO workflow config
│   │   ├── gsea_config.yaml     # GSEA workflow config
│   │   └── batch_go_config.yaml # Batch GO workflow config
│   ├── rules/                   # Additional Snakemake rules (optional)
│   └── scripts/                 # Workflow helper scripts (optional)
│
├── data/                         # Data directory (gitignored)
│   ├── raw/                     # Raw input files
│   └── processed/               # Intermediate processed data
│
├── notebooks/                    # Interactive Jupyter notebooks
│   ├── GO_Pipeline.ipynb        # Guided GO analysis workflow
│   └── GSEA_Pipeline.ipynb      # Guided GSEA workflow
│
├── src/                          # Source code
│   ├── __init__.py
│   │
│   ├── analysis/                # Analysis modules (each is a CLI tool)
│   │   ├── data_loading.py     # Data standardization
│   │   ├── filtering.py        # DEG filtering
│   │   ├── volcano.py          # Volcano plots
│   │   ├── go_enrich.py        # GO enrichment
│   │   ├── go_barplot.py       # GO visualization
│   │   ├── gsea_analysis.py    # GSEA execution
│   │   ├── gsea_plot.py        # GSEA visualization
│   │   ├── report_generation.py # HTML report generation
│   │   ├── batch_runner.py     # Batch processing orchestrator
│   │   └── compare_degs.py     # Multi-sample comparison
│   │
│   ├── utils.py                 # Core utility functions
│   ├── io_utils.py             # File I/O utilities
│   ├── filter_utils.py         # Filtering utilities
│   └── viz_utils.py            # Visualization utilities
│
├── output/                       # Analysis outputs (gitignored)
│   └── <sample_name>/          # Per-sample results
│       ├── standardized.csv
│       ├── filtered.csv
│       ├── volcano.png
│       ├── go_results.csv
│       ├── go_barplot.png
│       └── report.html
│
├── results/                      # Batch processing results (gitignored)
│   └── batch_<timestamp>/      # Timestamped batch results
│
├── ref/                          # Reference files (download separately)
│   ├── go-basic.obo            # GO ontology
│   └── goa_*.gaf               # GO annotations
│
├── setup.py                      # Package installation configuration
├── MANIFEST.in                   # Package data files specification
├── requirements.txt              # Python dependencies (pip)
├── environment.yml               # Conda environment specification
├── snakemake_environment.yml     # Snakemake environment with all dependencies
├── CONTRIBUTING.md               # Contribution guidelines
├── .gitignore                   # Git ignore patterns
└── README.md                    # This file
```

### Module Organization Philosophy

The project follows a **"tools, not libraries"** philosophy:

- **Each module = One tool:** Every `.py` file in `src/analysis/` is a complete, runnable CLI tool
- **Composability:** Tools can be chained together or used independently
- **Reusability:** Utility functions in `src/*.py` are imported by analysis modules
- **Configurability:** All tools accept both CLI args and YAML configs
- **Testability:** Each module has a clear input → process → output pattern

## 📊 Output Files

Each analysis generates a structured set of outputs:

### Standard GO Analysis Output

```
output/<sample_name>/
├── standardized.csv              # Standardized input data
├── filtered.csv                  # Significant DEGs only
├── filtered_up_genes.txt         # Upregulated gene list
├── filtered_down_genes.txt       # Downregulated gene list
├── volcano.png                   # Volcano plot
├── go_results.csv               # All GO enrichment results
├── go_results_up.csv            # GO results for upregulated genes
├── go_results_down.csv          # GO results for downregulated genes
├── go_barplot.png               # GO terms bar plot
└── report.html                  # Comprehensive HTML report
```

### GSEA Output

```
output/<sample_name>/
├── standardized.csv              # Input data
├── gsea_<geneset>/              # Per-gene-set GSEA results
│   ├── gseapy_results.csv       # Enrichment statistics
│   ├── enrichment_plots/        # Individual pathway plots
│   └── summary.txt
├── gsea_summary_dotplot.png     # Multi-pathway summary
└── gsea_report.html             # GSEA HTML report
```

### Batch Processing Output

#### Python Batch Runner

```
results/batch_20231023_143022/
├── sample1/
│   └── [complete analysis outputs]
├── sample2/
│   └── [complete analysis outputs]
├── temp_config_sample1.yaml     # Generated configs (for debugging)
└── temp_config_sample2.yaml
```

#### Snakemake Batch Processing

```
results/batch_go_snakemake/
├── sample1/
│   ├── standardized.csv
│   ├── filtered.csv
│   ├── volcano.png
│   ├── goea_results_*.csv
│   ├── go_barplot_*.png
│   ├── report.html
│   ├── temp_config.yaml         # Sample-specific config
│   └── logs/                    # Detailed execution logs
│       ├── data_loading.log
│       ├── filtering.log
│       └── ...
├── sample2/
│   └── [complete analysis outputs]
└── sample3/
    └── [complete analysis outputs]
```

### HTML Report Contents

The automatically generated HTML reports include:

- **Summary Statistics:** Number of genes, DEGs, enriched terms
- **Volcano Plot:** Interactive visualization of differential expression
- **Top GO Terms:** Tables of most significant enriched terms
- **Enrichment Plots:** Bar/dot plots of GO or GSEA results
- **Methodology:** Analysis parameters and thresholds used
- **Metadata:** Timestamp, sample name, configuration

Reports are self-contained (embed images) and can be easily shared or archived.

## 🤝 Contributing

Contributions are welcome! This project values:

- **Modularity:** Keep components independent and reusable
- **Documentation:** Update docstrings and README for changes
- **Consistency:** Follow existing code style and patterns
- **Testing:** Ensure changes don't break existing functionality

### Development Setup

```bash
# Clone and setup
git clone <repo-url>
cd RNA-Seq_GO_GSEA_analysis
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install git+https://github.com/parkgilbong/YG_utils_analysis.git@main

# Make your changes
# Test with sample data
# Commit and push
```

### Code Style Guidelines

- Use **type hints** for function parameters and returns
- Write **comprehensive docstrings** following NumPy/Google style
- Keep functions **focused and single-purpose**
- Use **meaningful variable names**
- Add **examples in docstrings** where helpful

## 📚 Additional Resources

### Reference Data

Required reference files are not included in the repository due to size:

- **GO Ontology (OBO):** Download from [Gene Ontology](http://geneontology.org/docs/download-ontology/)
- **GO Annotations (GAF):** Download from [GOA](http://geneontology.org/docs/download-go-annotations/)
- **MSigDB Gene Sets:** Available at [MSigDB](https://www.gsea-msigdb.org/gsea/msigdb/)

Place reference files in the `ref/` directory.

### Tutorials and Documentation

- **[API Reference](docs/API_REFERENCE.md)** - Complete Python API documentation for programmatic usage
- **[Contributing Guide](CONTRIBUTING.md)** - Development setup and contribution guidelines
- [GO Enrichment Analysis Tutorial](docs/GO_tutorial.md) *(coming soon)*
- [GSEA Analysis Guide](docs/GSEA_guide.md) *(coming soon)*
- [Batch Processing Best Practices](docs/batch_processing.md) *(coming soon)*

### Related Tools and Resources

- [GOATOOLS](https://github.com/tanghaibao/goatools) - GO enrichment analysis
- [GSEApy](https://gseapy.readthedocs.io/) - Gene Set Enrichment Analysis
- [MSigDB](https://www.gsea-msigdb.org/gsea/msigdb/) - Molecular Signatures Database
- [Gene Ontology](http://geneontology.org/) - GO terms and annotations

## ❓ Support

### Getting Help

- **Issues:** Open an issue on GitHub for bugs or feature requests
- **Discussions:** Use GitHub Discussions for questions and ideas
- **Documentation:** Check this README and inline docstrings

### Common Issues

**Import errors for `utils.*`:**
- Ensure `YG_utils_analysis` package is installed
- Check that you're running from the project root directory

**Missing reference files:**
- Download required OBO and GAF files to `ref/` directory
- See "Additional Resources" section for download links

**Memory errors with large datasets:**
- Process samples in smaller batches
- Increase available RAM or use HPC resources
- Consider filtering input data before analysis

### Reporting Bugs

When reporting issues, please include:
- Python version and operating system
- Full error message and traceback
- Config file used (sanitized if needed)
- Steps to reproduce the issue

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **GOATOOLS** for GO enrichment analysis functionality
- **GSEApy** for GSEA implementation
- **YG_utils_analysis** for shared utility functions
- All contributors and users of this pipeline

## 📮 Contact

For questions, suggestions, or collaboration inquiries:
- Open an issue on GitHub
- Contact the maintainers through GitHub

---

**Note:** This pipeline is designed for research use. Always validate results and consult with bioinformatics experts when interpreting biological data.