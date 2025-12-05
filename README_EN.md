# RNA-Seq Post-Analysis Pipeline: GO and GSEA

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A comprehensive, modular Python pipeline for RNA-Seq post-analysis, specializing in **Gene Ontology (GO) Enrichment Analysis** and **Gene Set Enrichment Analysis (GSEA)**. Designed for both interactive exploration via Jupyter notebooks and high-throughput batch processing.

## 🎯 Key Highlights

- **🧩 Highly Modular:** Independent, reusable analysis modules that can be mixed and matched
- **⚙️ Configuration-Driven:** YAML-based configuration for reproducible analyses
- **🚀 Multiple Execution Modes:** Interactive notebooks, CLI tools, and Snakemake workflows
- **🐍 Snakemake Integration:** Automated workflow management with parallelization and error recovery
- **📊 Publication-Ready Outputs:** High-quality visualizations and comprehensive HTML reports
- **🔄 Efficient Batch Processing:** Process multiple samples in parallel using Snakemake
- **🐧 HPC-Ready:** Full support for SLURM, PBS, and other cluster schedulers

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [Snakemake Workflow Automation](#-snakemake-workflow-automation)
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
- **🐍 Snakemake Workflows:** Automated pipeline execution with dependency tracking
- **⚡ Parallel Processing:** Leverage multiple cores for faster batch analysis
- **🖥️ CLI Tools:** Full command-line interface for all analysis steps
- **🔄 Reproducibility:** Configuration-based workflows ensure reproducible results
- **💾 Smart Caching:** Only re-run steps when inputs change (Snakemake)

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
- Python 3.9 or higher
- Conda package manager (recommended for easy setup)

### Recommended Installation with Conda

The easiest way to set up the environment is using the provided `environment.yml` file:

```bash
# 1. Clone the repository
git clone https://github.com/ibs-CMG-NGS/RNA-Seq_GO_GSEA_analysis.git
cd RNA-Seq_GO_GSEA_analysis

# 2. Create and activate conda environment with all dependencies
conda env create -f environment.yml
conda activate rnaseq-analysis

# 3. (Optional) Install package in development mode for CLI commands
pip install -e .
```

After installation with `-e .`, you can use convenient command aliases:
- `rnaseq-data-load` instead of `python src/analysis/data_loading.py`
- `rnaseq-filter` instead of `python src/analysis/filtering.py`
- `rnaseq-batch` instead of `python src/analysis/batch_runner.py`
- And more! See CLI Reference section for complete list.

### Installation for Snakemake Workflows

If you want to use Snakemake for workflow automation (recommended for batch processing):

```bash
# Create Snakemake environment with all dependencies
conda env create -f snakemake_environment.yml
conda activate snakemake_env
```

This environment includes Snakemake along with all analysis dependencies.

### Alternative Installation (pip + venv)

If you prefer using pip and virtual environments:

```bash
# 1. Clone the repository
git clone https://github.com/ibs-CMG-NGS/RNA-Seq_GO_GSEA_analysis.git
cd RNA-Seq_GO_GSEA_analysis

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Linux/macOS
# OR
venv\Scripts\activate     # On Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install the utility package dependency
pip install git+https://github.com/parkgilbong/YG_utils_analysis.git@main

# 5. (Optional) Install package in development mode for CLI commands
pip install -e .
```

### Verify Installation

```bash
# Test that modules can be imported
python -c "import pandas, gseapy, goatools; print('Installation successful!')"

# Check CLI tools
python src/analysis/data_loading.py --help

# If using Snakemake environment, verify Snakemake is available
snakemake --version
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
# Method A: Using direct Python commands
python src/analysis/data_loading.py --config configs/GO_pipeline_Shank2.yaml --config-section data_loading
python src/analysis/filtering.py --config configs/GO_pipeline_Shank2.yaml --config-section filtering
python src/analysis/volcano.py --config configs/GO_pipeline_Shank2.yaml --config-section volcano
python src/analysis/go_enrich.py --config configs/GO_pipeline_Shank2.yaml --config-section go_enrich
python src/analysis/report_generation.py --config configs/GO_pipeline_Shank2.yaml --config-section report

# Method B: Using convenience scripts (recommended for Linux/Mac)
./scripts/run_go_pipeline.sh configs/GO_pipeline_Shank2.yaml

# Method C: Using installed CLI commands (after 'pip install -e .')
rnaseq-data-load --config configs/GO_pipeline_Shank2.yaml --config-section data_loading
rnaseq-filter --config configs/GO_pipeline_Shank2.yaml --config-section filtering
rnaseq-volcano --config configs/GO_pipeline_Shank2.yaml --config-section volcano
rnaseq-go-enrich --config configs/GO_pipeline_Shank2.yaml --config-section go_enrich
rnaseq-report --config configs/GO_pipeline_Shank2.yaml --config-section report
```

### Option 3: Batch Processing with Snakemake (Recommended)

**Snakemake** is a workflow management system that automates the execution of complex data analysis pipelines. It provides superior batch processing capabilities compared to sequential Python scripts.

#### Why Use Snakemake?

- **🔄 Automatic Parallelization**: Run independent samples in parallel automatically
- **📊 Dependency Tracking**: Only re-run steps when inputs change
- **🔍 Reproducibility**: Built-in provenance tracking and workflow documentation
- **⚡ Resource Management**: Efficient allocation of CPU/memory resources
- **🎯 Error Recovery**: Resume from where pipeline failed without restarting
- **📈 Scalability**: Seamlessly scale from laptop to HPC clusters
- **📉 Visualization**: Generate workflow DAGs for understanding pipeline structure

#### Setup Snakemake Environment

```bash
# Create and activate Snakemake environment
conda env create -f snakemake_environment.yml
conda activate snakemake_env
```

#### Run Batch GO Analysis

```bash
# Edit workflow/config/batch_go_config.yaml to specify your samples
# Then run:
snakemake --snakefile workflow/Snakefile_batch_GO \
    --configfile workflow/config/batch_go_config.yaml \
    --cores 4

# For dry-run (see what will be executed):
snakemake --snakefile workflow/Snakefile_batch_GO \
    --configfile workflow/config/batch_go_config.yaml \
    --dry-run
```

#### Run Single Sample Analysis

```bash
# GO enrichment analysis
snakemake --snakefile workflow/Snakefile_GO \
    --configfile workflow/config/go_config.yaml \
    --cores 1

# GSEA analysis
snakemake --snakefile workflow/Snakefile_GSEA \
    --configfile workflow/config/gsea_config.yaml \
    --cores 1
```

#### Visualize Workflow

```bash
# Generate workflow diagram (requires graphviz)
snakemake --snakefile workflow/Snakefile_GO \
    --configfile workflow/config/go_config.yaml \
    --dag | dot -Tpng > workflow_dag.png
```

#### HPC/Cluster Execution

For SLURM clusters:

```bash
snakemake --snakefile workflow/Snakefile_batch_GO \
    --configfile workflow/config/batch_go_config.yaml \
    --cluster "sbatch --time=02:00:00 --mem=16G --cpus-per-task=1" \
    --jobs 10
```

The Snakemake approach will:
- Process samples in parallel when resources allow
- Automatically manage dependencies between analysis steps
- Resume from failure points without re-running completed steps
- Generate detailed logs for each rule execution
- Create organized output directories per sample
- Track which files were generated and when

See the [Workflow README](workflow/README.md) for detailed Snakemake usage instructions.

### Option 4: Batch Processing with Python (Alternative)

For users who prefer Python-based batch processing or don't have Snakemake:

```bash
# Method A: Direct Python command
python src/analysis/batch_runner.py --manifest configs/batch_manifest_H2O2.yaml

# Method B: Using installed CLI (after 'pip install -e .')
rnaseq-batch --manifest configs/batch_manifest_H2O2.yaml
```

The Python batch runner will:
- Process each sample sequentially
- Generate sample-specific output directories
- Create temporary configurations per sample
- Log progress and errors for debugging

**Note**: While the Python batch runner is simpler, Snakemake offers better performance, 
error recovery, and scalability for processing multiple samples.

### Helper Scripts

The `scripts/` directory contains convenient wrapper scripts:

```bash
# Run complete GO pipeline
./scripts/run_go_pipeline.sh configs/GO_pipeline_Shank2.yaml

# Run complete GSEA pipeline
./scripts/run_gsea_pipeline.sh configs/GSEA_pipeline.yaml
```

These scripts:
- Run all pipeline steps automatically
- Show progress for each step
- Exit immediately if any step fails
- Work on Linux, macOS, and Windows (via Git Bash/WSL)

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

## 🐍 Snakemake Workflow Automation

Snakemake is a powerful workflow management system that brings reproducibility, scalability, and efficiency to your RNA-Seq analysis. This section provides comprehensive guidance on using Snakemake workflows.

### Why Snakemake?

Snakemake offers significant advantages over traditional sequential batch processing:

#### Key Benefits

1. **Automatic Parallelization**
   - Executes independent samples and steps in parallel
   - Maximizes resource utilization on multi-core systems
   - Reduces total analysis time by 3-5x for batch processing

2. **Smart Dependency Management**
   - Tracks input/output relationships automatically
   - Only re-runs steps when inputs change
   - Avoids redundant computations

3. **Reproducibility**
   - Built-in provenance tracking
   - Version-controlled workflow definitions
   - Documented execution history

4. **Error Recovery**
   - Resume from failure points without restarting
   - No need to re-run successful steps
   - Save time and computational resources

5. **Scalability**
   - Seamlessly scale from laptop to HPC clusters
   - Works with SLURM, PBS, LSF, and other schedulers
   - Cloud execution support (AWS, Google Cloud)

6. **Visualization**
   - Generate workflow DAGs
   - Understand pipeline structure at a glance
   - Debug complex workflows easily

### Workflow Types

We provide three Snakemake workflows:

1. **`Snakefile_GO`** - Single-sample GO enrichment analysis
2. **`Snakefile_GSEA`** - Single-sample GSEA analysis
3. **`Snakefile_batch_GO`** - Multi-sample batch GO analysis

### Quick Start with Snakemake

#### 1. Setup Environment

```bash
# Create and activate Snakemake environment
conda env create -f snakemake_environment.yml
conda activate snakemake_env
```

#### 2. Configure Your Analysis

Edit the workflow configuration file for your analysis type:

```bash
# For single GO analysis
nano workflow/config/go_config.yaml

# For batch GO analysis
nano workflow/config/batch_go_config.yaml
```

#### 3. Dry Run (Preview)

Always preview what will be executed:

```bash
# Single sample GO analysis
snakemake --snakefile workflow/Snakefile_GO \
    --configfile workflow/config/go_config.yaml \
    --dry-run --printshellcmds

# Batch GO analysis
snakemake --snakefile workflow/Snakefile_batch_GO \
    --configfile workflow/config/batch_go_config.yaml \
    --dry-run --printshellcmds
```

#### 4. Execute Workflow

```bash
# Single sample (1 core)
snakemake --snakefile workflow/Snakefile_GO \
    --configfile workflow/config/go_config.yaml \
    --cores 1

# Batch processing (4 cores for parallel execution)
snakemake --snakefile workflow/Snakefile_batch_GO \
    --configfile workflow/config/batch_go_config.yaml \
    --cores 4
```

### Advanced Snakemake Usage

#### Workflow Visualization

Generate visual representations of your workflow:

```bash
# DAG (Directed Acyclic Graph) showing all jobs
snakemake --snakefile workflow/Snakefile_GO \
    --configfile workflow/config/go_config.yaml \
    --dag | dot -Tpng > workflow_dag.png

# Rule graph showing workflow structure
snakemake --snakefile workflow/Snakefile_GO \
    --configfile workflow/config/go_config.yaml \
    --rulegraph | dot -Tpng > workflow_rules.png

# File graph showing input/output dependencies
snakemake --snakefile workflow/Snakefile_GO \
    --configfile workflow/config/go_config.yaml \
    --filegraph | dot -Tpng > workflow_files.png
```

#### Executing Specific Rules

Run only certain steps of the pipeline:

```bash
# Run only data loading and filtering
snakemake --snakefile workflow/Snakefile_GO \
    --configfile workflow/config/go_config.yaml \
    --until filtering --cores 1

# Run only the GO enrichment step
snakemake --snakefile workflow/Snakefile_GO \
    --configfile workflow/config/go_config.yaml \
    --forcerun go_enrich --cores 1
```

#### Force Re-execution

Force re-running of specific steps or entire workflow:

```bash
# Re-run entire workflow
snakemake --snakefile workflow/Snakefile_GO \
    --configfile workflow/config/go_config.yaml \
    --forceall --cores 1

# Re-run from a specific rule onwards
snakemake --snakefile workflow/Snakefile_GO \
    --configfile workflow/config/go_config.yaml \
    --forcerun go_enrich --cores 1
```

#### Cluster/HPC Execution

##### SLURM Clusters

```bash
# Basic SLURM submission
snakemake --snakefile workflow/Snakefile_batch_GO \
    --configfile workflow/config/batch_go_config.yaml \
    --cluster "sbatch --time=02:00:00 --mem=16G --cpus-per-task=1" \
    --jobs 10

# With custom resource allocation per rule
snakemake --snakefile workflow/Snakefile_batch_GO \
    --configfile workflow/config/batch_go_config.yaml \
    --cluster "sbatch --time={resources.time} --mem={resources.mem_mb}M" \
    --default-resources time=60 mem_mb=8000 \
    --jobs 20
```

##### PBS/Torque Clusters

```bash
snakemake --snakefile workflow/Snakefile_batch_GO \
    --configfile workflow/config/batch_go_config.yaml \
    --cluster "qsub -l walltime=02:00:00 -l mem=16gb" \
    --jobs 10
```

#### Monitoring and Logging

```bash
# Detailed progress logging
snakemake --snakefile workflow/Snakefile_batch_GO \
    --configfile workflow/config/batch_go_config.yaml \
    --cores 4 \
    --printshellcmds \
    --verbose

# Save logs to file
snakemake --snakefile workflow/Snakefile_batch_GO \
    --configfile workflow/config/batch_go_config.yaml \
    --cores 4 \
    2>&1 | tee snakemake_run.log
```

### Batch Configuration Example

Here's a complete example of `workflow/config/batch_go_config.yaml`:

```yaml
# Output directory for all samples
output_root: "results/batch_go_snakemake"

# Base configuration applied to all samples
base_config:
  filtering:
    mode: thresholds
    padj_cutoff: 0.05
    log2fc_cutoff: 0
    direction: both
  
  go_enrich:
    obo: "ref/go-basic.obo"
    gaf: "ref/goa_mouse.gaf"
    taxon: 10090
    alpha: 0.05

# Sample definitions
samples:
  - name: "Control_vs_Treatment1"
    overrides:
      data_loading:
        excel_path: "data/exp1.xlsx"
        sheets: "Sheet1"
        gene_col: "Gene Symbol"
        log2fc_col: "log2FC"
        padj_col: "padj"
      report:
        title: "GO Analysis: Control vs Treatment1"
        sample_name: "Treatment1"
  
  - name: "Control_vs_Treatment2"
    overrides:
      data_loading:
        excel_path: "data/exp2.xlsx"
        sheets: "Sheet1"
      filtering:
        padj_cutoff: 0.01  # Stricter threshold for this sample
      report:
        title: "GO Analysis: Control vs Treatment2"
        sample_name: "Treatment2"
```

### Troubleshooting

#### Common Issues

**Issue**: "MissingInputException: Missing input files"
```bash
# Solution: Check if input files exist and paths are correct
snakemake --snakefile workflow/Snakefile_GO \
    --configfile workflow/config/go_config.yaml \
    --dry-run --verbose
```

**Issue**: "AmbiguousRuleException"
```bash
# Solution: Be more specific with target files or rules
snakemake --snakefile workflow/Snakefile_GO \
    --configfile workflow/config/go_config.yaml \
    --until rule_name --cores 1
```

**Issue**: Jobs fail but Snakemake doesn't show errors
```bash
# Solution: Check log files in output directory
cat results/batch_go_snakemake/sample1/logs/*.log
```

### Performance Optimization

For optimal performance when processing multiple samples:

```bash
# Use appropriate core count (typically: number of samples or CPU cores)
# Example: 8 samples on a 16-core machine
snakemake --snakefile workflow/Snakefile_batch_GO \
    --configfile workflow/config/batch_go_config.yaml \
    --cores 8

# For cluster execution, match jobs to available nodes
# Example: 50 samples on cluster with 10 available nodes
snakemake --snakefile workflow/Snakefile_batch_GO \
    --configfile workflow/config/batch_go_config.yaml \
    --cluster "sbatch --time=02:00:00 --mem=16G" \
    --jobs 10
```

### Best Practices

1. **Always dry-run first**: Use `--dry-run` to preview execution
2. **Use version control**: Commit workflow and config files to git
3. **Document parameters**: Add comments to configuration files
4. **Check logs**: Review execution logs for errors and warnings
5. **Visualize workflows**: Generate DAGs to understand pipeline structure
6. **Start small**: Test with 1-2 samples before full batch processing
7. **Monitor resources**: Track memory and CPU usage during execution
8. **Use appropriate cores**: Match `--cores` to your system capabilities

### Additional Resources

- **Workflow README**: See `workflow/README.md` for detailed workflow documentation
- **Snakemake Documentation**: https://snakemake.readthedocs.io/
- **Tutorial**: https://snakemake.readthedocs.io/en/stable/tutorial/tutorial.html
- **Best Practices**: https://snakemake.readthedocs.io/en/stable/snakefiles/best_practices.html

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

### Using Custom Gene Sets for GSEA

You can use your own custom gene sets for GSEA analysis by placing them in the `ref/` directory. Gene sets should be in **GMT format** (Gene Matrix Transposed).

#### GMT Format Structure

A GMT file is a tab-delimited text file where each line represents a gene set:

```
PATHWAY_NAME    DESCRIPTION    GENE1    GENE2    GENE3    ...
```

**Example GMT file** (`ref/my_custom_pathways.gmt`):
```
SYNAPSE_GENES    Synaptic_Function_Related    Shank1    Shank2    Shank3    Dlg4    Syngap1
GABA_SIGNALING    GABAergic_Neurotransmission    Gad1    Gad2    Slc32a1    Gabra1    Gabrb2
GLUTAMATE_RECEPTORS    Glutamatergic_Signaling    Grin1    Grin2a    Grin2b    Gria1    Gria2
```

Each line contains:
1. **Gene set name** (e.g., `SYNAPSE_GENES`)
2. **Description** (e.g., `Synaptic_Function_Related`)
3. **Gene symbols** (tab-separated, e.g., `Shank1    Shank2    Shank3`)

#### Where to Obtain Gene Sets

**1. MSigDB (Molecular Signatures Database)**
- Visit [MSigDB Downloads](https://www.gsea-msigdb.org/gsea/msigdb/collections.jsp)
- Choose appropriate collection:
  - **H: Hallmark gene sets** - Well-defined biological states/processes
  - **C2: Curated gene sets** - From online pathway databases (KEGG, Reactome, BioCarta)
  - **C5: Ontology gene sets** - Gene Ontology terms
  - **C6: Oncogenic signatures** - Cancer-related signatures
- Select organism (Human or Mouse)
- Download as GMT file

**2. Custom Gene Sets from Literature**
- Extract gene lists from published papers
- Create your own GMT file with genes of interest
- Group genes by functional categories or pathways

**3. GO Terms**
- Convert GO annotations to GMT format
- Use specific GO terms relevant to your research

**4. Tissue/Cell-Type Specific Markers**
- Use marker genes from single-cell RNA-seq databases
- CellMarker database: [http://xteam.xbio.top/CellMarker/](http://xteam.xbio.top/CellMarker/)
- PanglaoDB: [https://panglaodb.se/](https://panglaodb.se/)

#### Using Custom Gene Sets in Analysis

**In YAML configuration** (`workflow/config/gsea_config.yaml`):

```yaml
gsea_analysis:
  mode: prerank  # or "classic"
  
  # Use your custom gene set file
  gene_sets:
    - "ref/my_custom_pathways.gmt"
    - "ref/synapse_related_genes.gmt"
  
  # Or use MSigDB collections
  # gene_sets:
  #   - "ref/h.all.v2025.1.Mm.symbols.gmt"     # Hallmark
  #   - "ref/c2.cp.kegg.v2025.1.Mm.symbols.gmt"  # KEGG pathways
  
  min_size: 5      # Minimum genes in a gene set
  max_size: 500    # Maximum genes in a gene set
  permutation_num: 1000
```

**Example: Creating a Custom Autism-Related Gene Set**

```bash
# Create custom GMT file
cat > ref/autism_gene_sets.gmt << EOF
ASD_RISK_GENES	Autism_Spectrum_Disorder_Risk_Genes	CHD8	SHANK3	NLGN3	NRXN1	SCN2A	SYNGAP1	PTEN	TSC1	TSC2
SYNAPTIC_ADHESION	Synaptic_Adhesion_Molecules	NLGN1	NLGN2	NLGN3	NLGN4X	NRXN1	NRXN2	NRXN3	LRRTM1	LRRTM2
EXCITATORY_SYNAPSE	Excitatory_Synapse_Proteins	DLG4	GRIN1	GRIN2A	GRIN2B	SHANK1	SHANK2	SHANK3	HOMER1	SYNGAP1
EOF
```

Then use it in your analysis:
```yaml
gsea_analysis:
  gene_sets:
    - "ref/autism_gene_sets.gmt"
```

#### Best Practices for Custom Gene Sets

1. **Gene Symbol Format**: Ensure gene symbols match your data (human: UPPERCASE, mouse: Capitalize)
2. **Size Constraints**: Keep gene sets between 5-500 genes for meaningful enrichment
3. **Documentation**: Include descriptive names and descriptions in your GMT file
4. **Version Control**: Keep GMT files in version control with your analysis
5. **Validation**: Test with a small subset before running full analysis
6. **Organism Compatibility**: Match gene sets to your organism (human vs mouse)

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