# RNA-Seq Post-Analysis Pipeline: GO and GSEA

This repository contains a comprehensive Python-based pipeline for post-analysis of RNA-Seq data, focusing on **Gene Ontology (GO) Enrichment Analysis** and **Gene Set Enrichment Analysis (GSEA)**. The pipeline is highly modular and configurable, designed to be run step-by-step via Jupyter Notebooks or in an automated fashion for multiple samples using a batch runner.

## Features

- **Modular Pipeline:** Analysis is broken down into sequential, independent scripts.
- **Configurability:** All steps are controlled by easy-to-edit YAML configuration files.
- **Dual Workflows:** Separate, guided notebooks for GO analysis (`GO_pipeline.ipynb`) and GSEA (`GSEA_pipeline.ipynb`).
- **Interactive & Automated Execution:** Run analyses interactively in the notebooks or process multiple samples at once with the batch runner.
- **Comprehensive Analysis:**
    - **Data Loading:** Standardizes and loads data from Excel files.
    - **Gene Filtering:** Filters differentially expressed genes (DEGs) based on p-value and log2-fold-change thresholds.
    - **GO Enrichment:** Performs GO analysis using `goatools`.
    - **GSEA:** Runs Gene Set Enrichment Analysis using `gseapy` against MSigDB collections or custom GMT files.
    - **Visualization:** Generates volcano plots, GO term bar plots, and GSEA summary plots (dot plots, bar plots).
    - **Reporting:** Automatically generates a final HTML report summarizing the results.
- **Batch Processing:** Efficiently run the entire pipeline for multiple samples defined in a manifest file.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/parkgilbong/RNA-Seq_GOEA.git
    cd RNA-Seq_GOEA
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    # source venv/bin/activate
    ```

3.  **Install dependencies:**
    This project requires packages listed in `requirements.txt` as well as the `YG_utils_analysis` package.

    ```bash
    # 1. Install standard packages from requirements.txt
    pip install -r requirements.txt

    # 2. Install the YG_utils_analysis package.
    pip install git+https://github.com/parkgilbong/YG_utils_analysis.git@main
    ```

## Usage

The main, guided workflows are managed in the `notebooks/` directory. These are the recommended starting points for running a single, complete analysis.

#### A. GO Enrichment Analysis

Use `notebooks/GO_Pipeline.ipynb` for a standard DEG-based GO enrichment workflow.

**Pipeline Stages:**
1.  `data_loading.py`: Loads and standardizes input data.
2.  `filtering.py`: Filters for significant DEGs.
3.  `volcano.py`: Generates a volcano plot.
4.  `go_enrich.py`: Performs GO enrichment analysis.
5.  `go_barplot.py`: Creates bar plots of top GO terms.
6.  `report_generation.py`: Compiles all results into an HTML report.

#### B. Gene Set Enrichment Analysis (GSEA)

Use `notebooks/GSEA_Pipeline.ipynb` for running GSEA (Pre-ranked or Classic).

**Pipeline Stages:**
1.  `data_loading.py`: Loads and standardizes data, creating ranked lists or expression matrices.
2.  `gsea_analysis.py`: Performs GSEA against specified gene set libraries.
3.  `gsea_plot.py`: Generates summary dot plots and bar plots from GSEA results.

**How to run:**
1.  Choose the appropriate notebook for your analysis (`GO_Pipeline.ipynb` or `GSEA_Pipeline.ipynb`).
2.  Open and run it in a Jupyter environment.
3.  Follow the instructions in the notebook. You will primarily need to select and modify a main configuration file (e.g., `configs/GO_pipeline_Shank2.yaml` or `configs/GSEA_pipeline.yaml`).
4.  Each step in the notebook calls the corresponding Python script, using a specific section of the YAML file for its settings.
    

### 2. Automated Batch Processing

For running the pipeline on multiple samples automatically, use the `src/analysis/batch_runner.py` script.

**How to run:**
1.  **Create a manifest file:** Define your samples and any configuration overrides in a manifest file, such as `configs/batch_manifest.yaml`. This file specifies the base configuration and the list of samples to process.
2.  **Execute the batch runner:** Run the script from your terminal, pointing to your manifest file.

    ```bash
    python src/analysis/batch_runner.py --manifest configs/batch_manifest_H2O2.yaml
    ```
3.  The script will iterate through each sample, generate a temporary configuration, and run the entire pipeline. Results for each sample will be saved in a dedicated subfolder within the specified output directory.

## Configuration

The pipeline's behavior is controlled by YAML files located in the `configs/` directory.

- **Pipeline Configs (`GO_pipeline_*.yaml`, `GSEA_pipeline.yaml`):** These are unified files containing sections for each analysis step (`data_loading`, `filtering`, `gsea`, etc.). This allows you to define all parameters for a full analysis in one place.
- **Batch Manifests (`batch_manifest_*.yaml`):** Specifies a `base_config_path` and a list of `samples`. Each sample can have `overrides` to customize parameters for that specific run. This is powerful for running either the GO or GSEA pipeline across many samples.

## Project Structure

```
RNA-Seq_GOEA/
├───configs/            # YAML configuration files for analyses and batches.
├───data/               # Raw and processed data.
├───notebooks/          # Jupyter notebooks, including the main GO_pipeline.ipynb.
├───output/             # Default directory for analysis results.
├───ref/                # Reference files (e.g., GO ontology files like go-basic.obo).
├───src/
│   ├───analysis/       # Core analysis scripts (data_loading, filtering, etc.).
│   │   └───batch_runner.py # Script for automated batch processing.
│   ├───...             # Other utility modules.
│   └───main.py         # An alternative entry point (less commonly used).
├───requirements.txt    # Python package dependencies.
└───README.md
```

## Output

- **Processed CSVs:** Standardized and filtered gene lists.
- **Plots:** Volcano plots, GO bar plots.
- **GO Results:** CSV files of enriched GO terms.
- **Reports:** HTML summary reports for each sample.
- **Batch Results:** Organized in subfolders under `output/go_analysis_results/`.

## Support

For questions or issues, please open an issue on GitHub or contact the project maintainer.