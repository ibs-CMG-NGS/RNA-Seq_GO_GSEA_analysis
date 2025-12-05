# Snakemake Workflows for RNA-Seq Analysis

This directory contains Snakemake workflow files for automating RNA-Seq post-analysis pipelines.

## ⚠️ Important: Run from Project Root

**Always run Snakemake commands from the project root directory**, not from the `workflow/` directory.

```bash
# ✅ CORRECT
cd /path/to/RNA-Seq_GO_GSEA_analysis
snakemake --snakefile Snakefile_GO --configfile configs/GO_pipeline_Shank2.yaml --cores 4

# ❌ WRONG - Don't run from workflow directory
cd workflow
snakemake --snakefile Snakefile_GO ...  # This will break path resolution!
```

---

## 📁 Workflow Files

### Single Sample Workflows

- **Snakefile_GO**: Gene Ontology enrichment analysis pipeline for a single sample
- **Snakefile_GSEA**: Gene Set Enrichment Analysis pipeline for a single sample

### Batch Processing Workflow

- **Snakefile_batch_GO**: Batch processing of multiple samples through the GO enrichment pipeline

---

## 🎯 Configuration Files

### Two-Tier Config System

1. **Default Templates** (`configs/templates/`) - **Do NOT edit directly**
   - `go_config.yaml` - GO pipeline defaults
   - `gsea_config.yaml` - GSEA pipeline defaults  
   - `batch_go_config_*.yaml` - Batch processing defaults

2. **Project Configs** (`configs/`) - **Edit these for your projects**
   - `GO_pipeline_Shank2.yaml` - Shank2 sample config
   - `GO_pipeline_H2O2.yaml` - H2O2 sample config
   - `GO_pipeline_CHD8.yaml` - CHD8 sample config

See [CONFIG_STRUCTURE.md](../CONFIG_STRUCTURE.md) for detailed documentation.

---

## 🚀 Quick Start

### Run GO Analysis (Single Sample)

```bash
# 1. Navigate to project root (REQUIRED!)
cd /path/to/RNA-Seq_GO_GSEA_analysis

# 2. Run with project-specific config
snakemake --snakefile Snakefile_GO \
          --configfile configs/GO_pipeline_Shank2.yaml \
          --cores 4 --use-conda

# 3. Dry-run first to check (recommended)
snakemake -n --snakefile Snakefile_GO \
          --configfile configs/GO_pipeline_Shank2.yaml
```

### Run GSEA Analysis (Single Sample)

```bash
cd /path/to/RNA-Seq_GO_GSEA_analysis

snakemake --snakefile Snakefile_GSEA \
          --configfile configs/GSEA_pipeline_Shank2.yaml \
          --cores 4 --use-conda
```

### Run Batch GO Analysis (Multiple Samples)

```bash
cd /path/to/RNA-Seq_GO_GSEA_analysis

snakemake --snakefile Snakefile_batch_GO \
          --configfile configs/templates/batch_go_config_Shank.yaml \
          --cores 4 --use-conda
```

---

## 📝 Creating Your Own Project Config

```bash
# 1. Copy existing config as template
cp configs/GO_pipeline_Shank2.yaml configs/GO_pipeline_MyProject.yaml

# 2. Edit the new config
nano configs/GO_pipeline_MyProject.yaml

# 3. Update at minimum:
#    - ROOT_DIR: output directory
#    - data_loading.excel_path: your data file
#    - data_loading.sheets: sheet name(s)
#    - report.sample_name: your sample name

# 4. Run with your config
snakemake --snakefile Snakefile_GO \
          --configfile configs/GO_pipeline_MyProject.yaml \
          --cores 4
```

---

## 🔍 Troubleshooting

### File Not Found Errors

If you see errors like:
```
Excel not found: /wrong/path/to/file.xlsx
```

**Check:**
1. ✅ Are you in project root? (`pwd` should end with `RNA-Seq_GO_GSEA_analysis`)
2. ✅ Is the path in your config relative to project root?
3. ✅ Does the file exist? (`ls -la data/`)

### Config Not Taking Effect

**Solution:** Make sure you're using `--configfile` with your project config:
```bash
snakemake --snakefile Snakefile_GO \
          --configfile configs/YOUR_CONFIG.yaml \  # ← Don't forget this!
          --cores 4
```

---

## 📚 Additional Documentation

- [CONFIG_STRUCTURE.md](../CONFIG_STRUCTURE.md) - Detailed config organization guide
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Snakemake command reference
- [../README.md](../README.md) - Main project documentation

---bash
# Option 1: Using helper script (recommended)
./workflow/scripts/run_snakemake_go.sh configs/templates/batch_go_config.yaml --batch

# Option 2: Direct Snakemake command
snakemake --snakefile Snakefile_batch_GO --configfile configs/templates/batch_go_config.yaml --cores 4
```

## Workflow Visualization

You can visualize the workflow DAG (Directed Acyclic Graph):

```bash
# Generate workflow diagram
snakemake --snakefile Snakefile_GO --configfile configs/templates/go_config.yaml --dag | dot -Tpng > dag.png

# Generate rule graph
snakemake --snakefile Snakefile_GO --configfile configs/templates/go_config.yaml --rulegraph | dot -Tpng > rulegraph.png
```

## Dry Run

Before running the actual analysis, you can perform a dry run to see what would be executed:

```bash
snakemake --snakefile Snakefile_GO --configfile configs/templates/go_config.yaml --dry-run
```

## Parallel Execution

Snakemake can execute independent tasks in parallel. Use the `--cores` parameter:

```bash
# Use 4 CPU cores
snakemake --snakefile Snakefile_batch_GO --configfile configs/templates/batch_go_config.yaml --cores 4

# Use all available cores
snakemake --snakefile Snakefile_batch_GO --configfile configs/templates/batch_go_config.yaml --cores all
```

## Cluster Execution

For HPC clusters with SLURM:

```bash
snakemake --snakefile Snakefile_batch_GO \
    --configfile configs/templates/batch_go_config.yaml \
    --cluster "sbatch --time=01:00:00 --mem=8G" \
    --jobs 10
```

## Directory Structure

```
workflow/
├── Snakefile_GO              # GO analysis workflow
├── Snakefile_GSEA            # GSEA analysis workflow
├── Snakefile_batch_GO        # Batch GO analysis workflow
├── config/                   # Configuration files
│   ├── go_config.yaml
│   ├── gsea_config.yaml
│   └── batch_go_config.yaml
├── rules/                    # Additional rule files (optional)
└── scripts/                  # Helper scripts (optional)
```
