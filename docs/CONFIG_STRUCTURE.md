# Configuration Structure Guide

## 📁 Configuration File Organization

### Directory Structure

```
RNA-Seq_GO_GSEA_analysis/
│
├── configs/                          # 🎯 PROJECT-SPECIFIC CONFIGS (User edits here)
│   ├── GO_pipeline_Shank2.yaml      # Shank2 sample config
│   ├── GO_pipeline_H2O2.yaml        # H2O2 sample config
│   ├── GO_pipeline_CHD8.yaml        # CHD8 sample config
│   ├── deg_comparison_*.yaml        # Standalone DEG comparison configs
│   ├── gene_filter_*.yaml           # Standalone gene filter configs
│   └── genes_of_interest.txt        # Gene lists
│
└── workflow/
    ├── Snakefile_GO                 # Main GO pipeline workflow
    ├── Snakefile_GSEA               # Main GSEA pipeline workflow
    ├── Snakefile_batch_GO           # Batch GO processing workflow
    │
    └── config/                      # 📋 DEFAULT TEMPLATES (Do not edit directly)
        ├── go_config.yaml           # GO pipeline default template
        ├── gsea_config.yaml         # GSEA pipeline default template
        └── batch_go_config_*.yaml   # Batch processing templates
```

---

## 🎯 Configuration Strategy

### Two-Tier Configuration System

1. **Default Templates** (`configs/templates/`)
   - Provides sensible defaults for all parameters
   - Should NOT be edited directly
   - Used as fallback when project config doesn't specify a value

2. **Project-Specific Configs** (`configs/`)
   - Override defaults for specific projects/samples
   - This is where YOU make changes
   - Git-tracked for reproducibility

### How Configuration Merging Works

When you run:
```bash
snakemake --snakefile Snakefile_GO \
          --configfile configs/GO_pipeline_Shank2.yaml \
          --cores 4
```

Snakemake does:
1. Loads `configs/templates/go_config.yaml` (defaults from `configfile:` in Snakefile)
2. Merges with `configs/GO_pipeline_Shank2.yaml` (from `--configfile`)
3. Project config values **override** default template values

---

## 📝 Creating a New Project Config

### Option 1: Copy and Edit Existing Config

```bash
# Copy template
cp configs/GO_pipeline_Shank2.yaml configs/GO_pipeline_MyProject.yaml

# Edit the new file
nano configs/GO_pipeline_MyProject.yaml
```

### Option 2: Use Minimal Config (Recommended)

Create `configs/GO_pipeline_MyProject.yaml` with only what you need to override:

```yaml
# Minimal project config - only override what's different
ROOT_DIR: "output/MyProject_analysis"

data_loading:
  excel_path: "data/MyProject_results.xlsx"
  sheets: "Sheet1"
  gene_col: "Gene_Symbol"
  log2fc_col: "logFC"
  padj_col: "adj.P.Val"

filtering:
  padj_cutoff: 0.01
  log2fc_cutoff: 1.0

report:
  sample_name: "MyProject Sample A"
  author: "Your Name"
```

All other parameters will use defaults from `configs/templates/go_config.yaml`.

---

## 🚀 Running Workflows

### ✅ CORRECT: Run from Project Root

```bash
# 1. Navigate to project root
cd /home/ngs/ngs-pipeline/RNA-Seq_GO_GSEA_analysis

# 2. Run Snakemake with project config
snakemake --snakefile Snakefile_GO \
          --configfile configs/GO_pipeline_Shank2.yaml \
          --cores 4 --use-conda
```

**Why this works:**
- All relative paths in config are resolved from project root
- Python scripts use `Path.cwd()` which will be project root
- Snakemake rules reference files relative to where you run the command

### ❌ INCORRECT: Run from Other Directories

```bash
# DON'T DO THIS - will fail with path errors
cd /home/ngs/somewhere_else
snakemake --snakefile /full/path/to/Snakefile_GO ...

# DON'T DO THIS - relative paths won't work
cd workflow
snakemake --snakefile Snakefile_GO ...
```

---

## 🔍 Path Resolution Rules

### All Paths are Relative to Project Root

When you specify paths in config files:

```yaml
# In configs/GO_pipeline_Shank2.yaml
data_loading:
  excel_path: "data/Shank2_RNA-seq_result.xlsx"  # ← Relative to project root

go_enrich:
  obo: "ref/go-basic.obo"                        # ← Relative to project root
  gaf: "ref/goa_mouse.gaf"                       # ← Relative to project root
```

They resolve to:
```
/home/ngs/ngs-pipeline/RNA-Seq_GO_GSEA_analysis/data/Shank2_RNA-seq_result.xlsx
/home/ngs/ngs-pipeline/RNA-Seq_GO_GSEA_analysis/ref/go-basic.obo
/home/ngs/ngs-pipeline/RNA-Seq_GO_GSEA_analysis/ref/goa_mouse.gaf
```

### Absolute Paths Also Work

```yaml
data_loading:
  excel_path: "/home/ngs/data/my_experiment.xlsx"  # Absolute path - used as-is
```

---

## 📚 Config File Types

### 1. Pipeline Configs (`configs/GO_pipeline_*.yaml`)
**Purpose**: Run complete GO enrichment pipeline via Snakemake  
**Usage**: `snakemake --snakefile Snakefile_GO --configfile configs/GO_pipeline_Shank2.yaml`  
**Contains**: All pipeline steps (data loading, filtering, GO analysis, plots, report)

### 2. DEG Comparison Configs (`configs/deg_comparison_*.yaml`)
**Purpose**: Compare DEGs across multiple datasets (standalone script)  
**Usage**: `python src/analysis/compare_degs.py --config configs/deg_comparison_Shank2.yaml`  
**Contains**: Multiple dataset paths and comparison settings

### 3. Gene Filter Configs (`configs/gene_filter_*.yaml`)
**Purpose**: Analyze specific genes across datasets (standalone script)  
**Usage**: `python src/analysis/gene_filter_analysis.py --config configs/gene_filter_Shank2.yaml`  
**Contains**: Gene list and visualization settings

---

## 🛠️ Troubleshooting

### "File not found" errors

**Problem**: `Excel not found: /home/ngs/.../data/processed/Shank2/file.xlsx`

**Solution**: Check these in order:
1. Are you running from project root? (`pwd` should show `RNA-Seq_GO_GSEA_analysis`)
2. Is the path in config correct relative to project root?
3. Does the file actually exist? (`ls -la data/`)

### Config values not taking effect

**Problem**: Your config changes don't seem to work

**Solution**:
1. Check you're using `--configfile configs/YOUR_CONFIG.yaml`
2. Verify the config section name matches what the script expects
3. Some values might be overridden by command-line arguments

### GO resources not found

**Problem**: `GO resources missing; skipping GOEA`

**Solution**:
```bash
# Check if reference files exist
ls -la ref/go-basic.obo
ls -la ref/goa_mouse.gaf

# If missing, check config has correct paths
grep -A5 "go_enrich:" configs/GO_pipeline_Shank2.yaml
```

---

## 📋 Best Practices

1. **Always run Snakemake from project root**
2. **Keep project configs in `configs/`** - easy to find and git-track
3. **Don't edit `configs/templates/` templates** - they're for defaults only
4. **Use meaningful config names** - e.g., `GO_pipeline_Shank2_3weeks.yaml`
5. **Comment your configs** - future you will thank you
6. **Test with dry-run first**: `snakemake -n --snakefile Snakefile_GO --configfile configs/YOUR_CONFIG.yaml`

---

## 🎓 Summary

| Aspect | Recommendation |
|--------|---------------|
| **Where to run** | Project root directory |
| **Which config to edit** | `configs/GO_pipeline_*.yaml` |
| **Template location** | `configs/templates/*.yaml` (read-only) |
| **Path convention** | Relative to project root |
| **Snakefile location** | `Snakefile_*` (don't move) |
| **Output location** | Specified in config `ROOT_DIR` |

