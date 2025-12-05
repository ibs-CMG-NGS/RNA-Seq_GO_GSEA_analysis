# Configuration Files Guide

## 📁 Directory Structure

```
configs/
├── 📘 README.md                       # This file
│
├── 🔵 Main GO Pipeline (for Snakemake)
│   ├── GO_pipeline_H2O2.yaml         # H2O2 sample - Complete pipeline config
│   ├── GO_pipeline_CHD8.yaml         # CHD8 sample - Complete pipeline config
│   └── GO_pipeline_Shank2.yaml       # Shank2 sample - Complete pipeline config
│
├── 🟢 Standalone DEG Comparison
│   ├── deg_comparison_template.yaml  # Template for new comparisons
│   ├── deg_comparison_H2O2.yaml      # H2O2 comparison config
│   └── deg_comparison_Shank2.yaml    # Shank2 comparison config
│
├── 🟡 Standalone Gene Filter
│   ├── gene_filter_template.yaml     # Template for new analyses
│   ├── gene_filter_H2O2.yaml         # H2O2 gene filter config
│   └── gene_filter_Shank2.yaml       # Shank2 gene filter config
│
├── � Resources
│   └── genes_of_interest.txt         # Example gene list
│
└── 🗂️ Legacy (archived - see legacy/README.md)
    ├── batch_manifest*.yaml          # Old batch configs (use Snakemake instead)
    ├── *_backup.yaml                 # Backup of old formats
    └── Single-step configs           # Use main config with --config-section instead
        ├── data_loading.yaml
        ├── filtering.yaml
        ├── volcano.yaml
        └── ... (9 files total)
```

**Note:** Single-step config files are no longer needed. All scripts support the `--config-section` parameter, allowing you to use the main config file and specify which section to use.

---

## 🎯 Configuration Types

### 1. **Main GO Pipeline Configs** (for Snakemake)

**Files:** `GO_pipeline_*.yaml`

**Purpose:** Configuration for the complete Snakemake GO enrichment pipeline

**Usage:**
```bash
snakemake -s workflow/Snakefile_GO --configfile workflow/config/go_config.yaml
```

**Contains:**
- Data loading parameters (Excel paths, column names)
- Filtering thresholds (p-value, log2FC cutoffs)
- Volcano plot settings
- GO enrichment parameters (taxon, alpha)
- Visualization options
- Report metadata

**Note:** File paths are managed by Snakemake rules, NOT in the config!

---

### 2. **DEG Comparison Configs** (standalone analysis)

**Files:** `deg_comparison_*.yaml`

**Purpose:** Compare two DEG result sets with Venn diagrams and heatmaps

**Usage:**
```bash
python src/analysis/compare_degs.py --config configs/deg_comparison_H2O2.yaml
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

**Files:** `gene_filter_*.yaml`

**Purpose:** Analyze specific genes of interest across multiple datasets

**Usage:**
```bash
python src/analysis/gene_filter_analysis.py --config configs/gene_filter_H2O2.yaml
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

1. Copy an existing GO pipeline config:
   ```bash
   cp configs/GO_pipeline_H2O2.yaml configs/GO_pipeline_MySample.yaml
   ```

2. Update the following:
   - `ROOT_DIR`: Output directory for your sample
   - `data_loading.excel_path`: Path to your input Excel file
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
