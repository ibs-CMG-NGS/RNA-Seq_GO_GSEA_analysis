# Configuration Files Guide

## 📁 Directory Structure

```
configs/
├── 📘 README.md                          # This file
│
├── � templates/                         # 📋 Template files (Git tracked)
│   ├── go_config.yaml                   # GO pipeline template
│   ├── gsea_config.yaml                 # GSEA pipeline template
│   ├── batch_go_config_*.yaml           # Batch GO templates
│   ├── GO_pipeline_example.yaml         # Complete example config
│   ├── deg_comparison_example.yaml      # DEG comparison example
│   └── gene_filter_example.yaml         # Gene filter example
│
├── � Your Project Configs (NOT in Git)  # ✏️ Create your configs here
│   ├── GO_pipeline_MyProject.yaml       # Your GO analysis config
│   ├── deg_comparison_MyData.yaml       # Your DEG comparison config
│   └── gene_filter_MyGenes.yaml         # Your gene filter config
│
└── 📄 genes_of_interest.txt             # Example gene list
```

## � Git Tracking

**Important:** Your personal configuration files in `configs/` are **NOT tracked by Git**!

- ✅ **Git tracked:** `configs/templates/*` (templates and examples)
- ✅ **Git tracked:** `configs/README.md` (this file)
- ❌ **Git ignored:** `configs/*.yaml` (your personal configs)

This means:
- You can safely create and modify your own config files
- Your configs won't be committed or pushed to the repository
- Template files remain available for everyone
- No risk of accidentally sharing sensitive file paths or parameters

---

## 🚀 Quick Start

### Creating Your First Config

```bash
# 1. Copy a template
cp configs/templates/GO_pipeline_example.yaml configs/GO_pipeline_MyProject.yaml

# 2. Edit your copy
nano configs/GO_pipeline_MyProject.yaml

# 3. Customize these key fields:
#    - ROOT_DIR: "output/my_analysis"
#    - data_loading.excel_path: "data/my_data.xlsx"
#    - data_loading.sheets: "Sheet1"
#    - report.sample_name: "My Sample"

# 4. Run analysis
snakemake --snakefile Snakefile_GO \
          --configfile configs/GO_pipeline_MyProject.yaml \
          --cores 4
```

---

## 🎯 Configuration Types

### 1. **Main GO Pipeline Configs** (for Snakemake)

**Template:** `templates/GO_pipeline_example.yaml`

**Purpose:** Configuration for the complete Snakemake GO enrichment pipeline

**Usage:**
```bash
snakemake --snakefile Snakefile_GO \
          --configfile configs/GO_pipeline_MyProject.yaml \
          --cores 4
```

**Contains:**
- Data loading parameters (Excel paths, column names)
- Filtering thresholds (p-value, log2FC cutoffs)
- Volcano plot settings
- GO enrichment parameters (taxon, alpha)
- Visualization options
- Report metadata

**Example:** See `templates/GO_pipeline_example.yaml` for a complete annotated example

---

### 2. **DEG Comparison Configs** (standalone analysis)

**Template:** `templates/deg_comparison_example.yaml`

**Purpose:** Compare two DEG result sets with Venn diagrams and heatmaps

**Usage:**
```bash
python src/analysis/compare_degs.py --config configs/deg_comparison_MyData.yaml
```

**Contains:**
- Input DEG files to compare
- Dataset names
- Visualization options (colors, sizes, etc.)
- Output file paths

**When to use:**
- Comparing different conditions
- Comparing different time points
- Overlap analysis between experiments

---

### 3. **Gene Filter Configs** (standalone analysis)

**Template:** `templates/gene_filter_example.yaml`

**Purpose:** Analyze specific genes of interest across multiple datasets

**Usage:**
```bash
python src/analysis/gene_filter_analysis.py --config configs/gene_filter_MyGenes.yaml
```

**Contains:**
- List of standardized CSV files to analyze
- Gene list file path
- Dot plot visualization options
- Output directory

**When to use:**
- Tracking specific genes across conditions
- Pathway-specific gene analysis
- Custom gene set visualization

---

## 🔧 How to Create New Configs

### For a New Sample (Main Pipeline):

1. **Copy the example template:**
   ```bash
   cp configs/templates/GO_pipeline_example.yaml configs/GO_pipeline_MySample.yaml
   ```

2. **Update key fields:**
   - `ROOT_DIR`: Output directory for your sample
   - `data_loading.excel_path`: Path to your input Excel file
   - `data_loading.sheets`: Sheet name(s) in your Excel file
   - `report.sample_name`: Name displayed in reports
   - `report.description`: Brief description of your analysis

3. **Adjust filtering thresholds (optional):**
   - `filtering.padj_threshold`: FDR threshold (default: 0.05)
   - `filtering.log2fc_threshold`: Log2 fold change threshold (default: 1.0)

4. **Run the pipeline:**
   ```bash
   snakemake --snakefile Snakefile_GO \
             --configfile configs/GO_pipeline_MySample.yaml \
             --cores 4
   ```

---

### For DEG Comparison:

1. **Copy the example:**
   ```bash
   cp configs/templates/deg_comparison_example.yaml configs/deg_comparison_MyComparison.yaml
   ```

2. **Edit input files:**
   ```yaml
   degs:
     file1: "data/processed/Sample1/standardized.csv"
     file2: "data/processed/Sample2/standardized.csv"
     name1: "Sample1"
     name2: "Sample2"
   ```

3. **Run comparison:**
   ```bash
   python src/analysis/compare_degs.py --config configs/deg_comparison_MyComparison.yaml
   ```

---

### For Gene Filter Analysis:

1. **Copy the example:**
   ```bash
   cp configs/templates/gene_filter_example.yaml configs/gene_filter_MyGenes.yaml
   ```

2. **Create your gene list** (`my_genes.txt`):
   ```
   Shank2
   Gabrg2
   Nlgn3
   Nrxn1
   ```

3. **Edit config:**
   ```yaml
   input:
     csv_files:
       - "data/processed/Sample1/standardized.csv"
       - "data/processed/Sample2/standardized.csv"
     gene_list: "my_genes.txt"
   ```

4. **Run analysis:**
   ```bash
   python src/analysis/gene_filter_analysis.py --config configs/gene_filter_MyGenes.yaml
   ```
   - `data_loading.sheets`: Sheet name(s) to load
   - `data_loading.*_col`: Column names in your Excel file
   - `report.sample_name`: Your sample name
   - `report.author`: Your name

3. Run the pipeline:
   ```bash
   # Copy to workflow config directory
   cp configs/GO_pipeline_MySample.yaml workflow/config/go_config.yaml
   
   # Run Snakemake
   snakemake -s workflow/Snakefile_GO --configfile workflow/config/go_config.yaml
   ```

---

### For DEG Comparison:

1. Copy the template:
   ```bash
   cp configs/deg_comparison_template.yaml configs/deg_comparison_MySample.yaml
   ```

2. Update:
   - `ROOT_DIR`: Base directory
   - `deg_comparison.file1`, `file2`: Paths to filtered CSV files
   - `deg_comparison.name1`, `name2`: Display names

3. Run:
   ```bash
   python src/analysis/compare_degs.py --config configs/deg_comparison_MySample.yaml
   ```

---

### For Gene Filter Analysis:

1. Copy the template:
   ```bash
   cp configs/gene_filter_template.yaml configs/gene_filter_MySample.yaml
   ```

2. Update:
   - `ROOT_DIR`: Base directory
   - `gene_filter.in_csv_files`: List of standardized CSV files
   - `gene_filter.file_aliases`: Display names
   - `gene_filter.gene_list_file`: Path to gene list

3. Run:
   ```bash
   python src/analysis/gene_filter_analysis.py --config configs/gene_filter_MySample.yaml
   ```

---

## 📝 Best Practices

### ✅ DO:
- Keep main GO pipeline configs focused on analysis parameters
- Use separate configs for different samples/experiments
- Use templates when creating new configs
- Document custom settings with comments

### ❌ DON'T:
- Mix file paths into main GO pipeline configs (Snakemake handles this)
- Hardcode absolute paths (use relative paths from project root)
- Reuse the same ROOT_DIR for different samples

---

## 🗂️ Config Organization

```
Main Snakemake Pipeline          Standalone Analysis Tools
        ↓                                  ↓
GO_pipeline_*.yaml          deg_comparison_*.yaml
                            gene_filter_*.yaml
        ↓                                  ↓
workflow/Snakefile_GO       Direct Python script execution
        ↓                                  ↓
Automated workflow          Custom/interactive analysis
```

---

## 💡 Examples

### Example 1: Run GO pipeline for Shank2 sample
```bash
cp configs/GO_pipeline_Shank2.yaml workflow/config/go_config.yaml
snakemake -s workflow/Snakefile_GO --configfile workflow/config/go_config.yaml -j 4
```

### Example 2: Run single step independently
```bash
# Run only filtering step using main config
python src/analysis/filtering.py \
  --config configs/GO_pipeline_H2O2.yaml \
  --config-section filtering \
  --in-csv data/processed/H2O2/standardized.csv \
  --out-csv data/processed/H2O2/filtered.csv \
  --out-up-genes data/processed/H2O2/filtered_up_genes.txt \
  --out-down-genes data/processed/H2O2/filtered_down_genes.txt

# Run only volcano plot using main config
python src/analysis/volcano.py \
  --config configs/GO_pipeline_H2O2.yaml \
  --config-section volcano \
  --in-csv data/processed/H2O2/standardized.csv \
  --out-png data/processed/H2O2/volcano.png
```

### Example 3: Compare two time points
```yaml
# configs/deg_comparison_H2O2_timepoints.yaml
deg_comparison:
  file1: "data/processed/H2O2/filtered_1d.csv"
  file2: "data/processed/H2O2/filtered_3d.csv"
  name1: "1 Day"
  name2: "3 Days"
```

```bash
python src/analysis/compare_degs.py --config configs/deg_comparison_H2O2_timepoints.yaml
```

### Example 4: Analyze specific genes
```bash
# First, create your gene list
echo -e "Apoe\nApp\nPsen1\nPsen2" > configs/my_genes.txt

# Update config to use this gene list
# gene_filter.gene_list_file: "configs/my_genes.txt"

python src/analysis/gene_filter_analysis.py --config configs/gene_filter_H2O2.yaml
```

---

## 🔍 Troubleshooting

**Q: Config section not found?**
- Check the `--config-section` parameter matches the section name in your YAML

**Q: File not found errors?**
- Verify paths are relative to project root
- Check ROOT_DIR is set correctly

**Q: Which config should I use?**
- For full pipeline: `GO_pipeline_*.yaml`
- For comparing results: `deg_comparison_*.yaml`
- For gene-specific analysis: `gene_filter_*.yaml`

**Q: What about batch_manifest files?**
- These are now in `legacy/` folder
- Use Snakemake batch workflows instead: `workflow/Snakefile_batch_GO`
- See `legacy/README.md` for migration guide

---

## 🗂️ Legacy Files

Old configuration formats and deprecated batch processing files are archived in the `legacy/` folder.

**What's there:**
- Old batch_manifest files (replaced by Snakemake workflows)
- Backup copies of refactored configs
- Documentation on migration

**Do I need them?**
- Generally no, if you're using the current Snakemake workflows
- Keep as reference if needed
- See `legacy/README.md` for details

---

## 📚 Related Documentation

- **Snakemake Workflow:** `workflow/README.md`
- **API Reference:** `docs/API_REFERENCE.md`
- **Pipeline Overview:** `README.md`
- **Legacy Files:** `legacy/README.md`
