# RNA-Seq Post-Analysis Pipeline: GO and GSEA

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A comprehensive, modular Python pipeline for RNA-Seq post-analysis, specializing in **Gene Ontology (GO) Enrichment Analysis** and **Gene Set Enrichment Analysis (GSEA)**. Designed for both interactive exploration via Jupyter notebooks and high-throughput batch processing.

## 🎯 Key Highlights

- **🧩 Highly Modular:** Independent, reusable analysis modules that can be mixed and matched
- **⚙️ Configuration-Driven:** YAML-based configuration for reproducible analyses
- **🚀 Dual Execution Modes:** Interactive notebooks for exploration + CLI tools for automation
- **📊 Publication-Ready Outputs:** High-quality visualizations and comprehensive HTML reports
- **🔄 Batch Processing:** Process multiple samples efficiently with a single command
- **🐧 Linux-Ready:** Full CLI support for server and HPC environments

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [Configuration](#-configuration)
- [CLI Reference](#-cli-reference)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [Support](#-support)

## ✨ Features

### Analysis Capabilities
- **📥 Data Loading & Standardization:** Load from Excel with flexible column mapping
- **🔍 Gene Filtering:** Filter DEGs by statistical thresholds or custom gene lists
- **🧬 GO Enrichment Analysis:** Comprehensive GO term enrichment using GOATOOLS
- **🎯 GSEA:** Pre-ranked and classic GSEA with MSigDB or custom gene sets
- **📈 Visualization Suite:**
  - Volcano plots with customizable annotation
  - GO term bar plots and dot plots
  - GSEA enrichment plots
  - Multi-condition comparison heatmaps
- **📄 Automated Reporting:** Generate comprehensive HTML reports with figures and tables

### Workflow Features
- **🔧 Modular Design:** Each analysis step is an independent, reusable module
- **📝 YAML Configuration:** All parameters controlled via human-readable config files
- **📓 Interactive Notebooks:** Step-by-step guided analysis for exploration
- **⚡ Batch Processing:** Process dozens of samples automatically via manifest files
- **🖥️ CLI Tools:** Full command-line interface for all analysis steps
- **🔄 Reproducibility:** Configuration-based workflows ensure reproducible results

## 🏗️ Architecture

The pipeline follows a **modular, Unix-philosophy design** where each analysis step:
- Is a self-contained Python script with its own CLI
- Reads configuration from YAML files
- Produces well-defined outputs (CSV, plots, reports)
- Can be run independently or as part of a pipeline

```
Input Data (Excel) → Data Loading → Filtering → Analysis (GO/GSEA) → Visualization → Report
                          ↓             ↓             ↓                    ↓
                        CSV          CSV         Results CSV           PNG/HTML
```

Each module can be:
- **Used standalone** via command line
- **Chained together** in notebooks for interactive analysis
- **Orchestrated** by the batch runner for high-throughput processing

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- (Optional) Conda for environment management

### Standard Installation

```bash
# 1. Clone the repository
git clone https://github.com/ibs-CMG-NGS/RNA-Seq_GO_GSEA_analysis.git
cd RNA-Seq_GO_GSEA_analysis

# 2. Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Linux/macOS
# OR
venv\Scripts\activate     # On Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install the utility package dependency
pip install git+https://github.com/parkgilbong/YG_utils_analysis.git@main
```

### Conda Installation (Alternative)

```bash
# Create conda environment
conda create -n rnaseq-analysis python=3.9
conda activate rnaseq-analysis

# Install dependencies
pip install -r requirements.txt
pip install git+https://github.com/parkgilbong/YG_utils_analysis.git@main
```

### Verify Installation

```bash
# Test that modules can be imported
python -c "import pandas, gseapy, goatools; print('Installation successful!')"

# Check CLI tools
python src/analysis/data_loading.py --help
```

## ⚡ Quick Start

### Option 1: Interactive Analysis (Notebooks)

Perfect for exploring a single sample or learning the pipeline.

```bash
# Start Jupyter
jupyter notebook

# Open one of the guided notebooks:
# - notebooks/GO_Pipeline.ipynb (for GO enrichment analysis)
# - notebooks/GSEA_Pipeline.ipynb (for GSEA analysis)
```

Each notebook provides:
- Step-by-step instructions
- Inline documentation
- Interactive parameter tuning
- Immediate visualization of results

### Option 2: CLI Single Analysis

Run individual analysis steps from the command line.

```bash
# 1. Load and standardize your data
python src/analysis/data_loading.py \
  --config configs/GO_pipeline_Shank2.yaml \
  --config-section data_loading

# 2. Filter for significant DEGs
python src/analysis/filtering.py \
  --config configs/GO_pipeline_Shank2.yaml \
  --config-section filtering

# 3. Generate volcano plot
python src/analysis/volcano.py \
  --config configs/GO_pipeline_Shank2.yaml \
  --config-section volcano

# 4. Run GO enrichment
python src/analysis/go_enrich.py \
  --config configs/GO_pipeline_Shank2.yaml \
  --config-section go_enrich

# 5. Generate report
python src/analysis/report_generation.py \
  --config configs/GO_pipeline_Shank2.yaml \
  --config-section report
```

### Option 3: Batch Processing

Process multiple samples automatically - ideal for HPC environments.

```bash
# Run entire pipeline for all samples defined in manifest
python src/analysis/batch_runner.py --manifest configs/batch_manifest_H2O2.yaml
```

The batch runner will:
- Process each sample sequentially
- Generate sample-specific output directories
- Create temporary configurations per sample
- Log progress and errors for debugging

## 📖 Usage Guide

### Interactive Analysis with Notebooks

The `notebooks/` directory contains guided Jupyter notebooks for interactive analysis.

#### GO Enrichment Analysis Pipeline

**Notebook:** `GO_Pipeline.ipynb`

**Pipeline Stages:**
1. **Data Loading** (`data_loading.py`) - Standardize Excel input files
2. **Filtering** (`filtering.py`) - Extract significant DEGs
3. **Volcano Plot** (`volcano.py`) - Visualize differential expression
4. **GO Enrichment** (`go_enrich.py`) - Identify enriched GO terms
5. **GO Visualization** (`go_barplot.py`) - Create bar/dot plots
6. **Report Generation** (`report_generation.py`) - Compile HTML report

**Configuration:** Edit `configs/GO_pipeline_*.yaml` files

#### GSEA Analysis Pipeline

**Notebook:** `GSEA_Pipeline.ipynb`

**Pipeline Stages:**
1. **Data Loading** (`data_loading.py`) - Prepare ranked gene lists or expression matrix
2. **GSEA Analysis** (`gsea_analysis.py`) - Run pre-ranked or classic GSEA
3. **GSEA Visualization** (`gsea_plot.py`) - Generate enrichment plots

**Configuration:** Edit `configs/GSEA_pipeline.yaml`

### Command-Line Analysis

Each module accepts both CLI arguments and YAML configuration. CLI arguments override config file values.

**Example: Running filtering with CLI overrides**

```bash
python src/analysis/filtering.py \
  --config configs/GO_pipeline_Shank2.yaml \
  --config-section filtering \
  --padj-cutoff 0.01 \
  --log2fc-cutoff 1.5 \
  --direction up
```

### Batch Processing

Create a manifest file defining your batch analysis:

```yaml
# configs/my_batch_manifest.yaml
base_config_path: "configs/GO_pipeline_template.yaml"
output_root: "results/my_batch_{timestamp}"

pipeline_steps:
  - data_loading
  - filtering
  - volcano
  - go_enrich
  - go_barplot
  - report_generation

samples:
  - name: "sample1"
    overrides:
      data_loading:
        excel_path: "data/sample1.xlsx"
  - name: "sample2"
    overrides:
      data_loading:
        excel_path: "data/sample2.xlsx"
```

Execute:
```bash
python src/analysis/batch_runner.py --manifest configs/my_batch_manifest.yaml
```

## ⚙️ Configuration

The pipeline uses YAML configuration files for all parameters. This design enables:
- **Reproducibility:** Same config = same results
- **Version Control:** Track parameter changes in git
- **Documentation:** Self-documenting analysis parameters

### Configuration Types

#### 1. Pipeline Configuration Files

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

All analysis modules support a consistent CLI interface:

```bash
python src/analysis/<module>.py --config <config.yaml> --config-section <section>
```

### Core Analysis Modules

| Module | Purpose | Key Parameters |
|--------|---------|----------------|
| `data_loading.py` | Load and standardize input data | `--excels`, `--sheets`, `--gene-col` |
| `filtering.py` | Filter DEGs by thresholds | `--padj-cutoff`, `--log2fc-cutoff`, `--direction` |
| `volcano.py` | Generate volcano plots | `--padj-cutoff`, `--log2fc-cutoff`, `--xlim`, `--ylim` |
| `go_enrich.py` | Run GO enrichment | `--genes-file`, `--background-csv`, `--obo`, `--gaf` |
| `go_barplot.py` | Visualize GO results | `--in-csv`, `--out-png`, `--top-terms` |
| `gsea_analysis.py` | Run GSEA | `--mode`, `--gene-sets`, `--min-size`, `--max-size` |
| `gsea_plot.py` | Visualize GSEA results | `--results-dir`, `--top-terms` |
| `report_generation.py` | Generate HTML report | All previous outputs |
| `batch_runner.py` | Batch processing | `--manifest` |

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
├── configs/                      # Configuration files
│   ├── GO_pipeline_*.yaml       # GO analysis configurations
│   ├── GSEA_pipeline.yaml       # GSEA configuration
│   ├── batch_manifest_*.yaml    # Batch processing manifests
│   └── genes_of_interest.txt    # Example gene lists
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
├── requirements.txt              # Python dependencies
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

```
results/batch_20231023_143022/
├── sample1/
│   └── [complete analysis outputs]
├── sample2/
│   └── [complete analysis outputs]
├── temp_config_sample1.yaml     # Generated configs (for debugging)
└── temp_config_sample2.yaml
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