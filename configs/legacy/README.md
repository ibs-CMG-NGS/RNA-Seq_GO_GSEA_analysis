# Legacy Configuration Files

This folder contains configuration files that are **no longer actively used** but are kept for reference purposes.

## 📜 Files in This Folder

### 1. Batch Manifest Files (Replaced by Snakemake)

- **batch_manifest.yaml**
- **batch_manifest_H2O2.yaml**
- **batch_manifest_Shank2.yaml**

**Previous Usage:**
```bash
python src/analysis/batch_runner.py --manifest configs/batch_manifest.yaml
```

**Replaced By:**
- Snakemake batch workflows: `workflow/Snakefile_batch_GO`
- New config format: `workflow/config/batch_go_config.yaml`

**Why Replaced:**
- ❌ Sequential execution (slow)
- ❌ No automatic dependency management
- ❌ Cannot restart from failure points
- ✅ Snakemake provides parallel execution, DAG-based dependencies, and automatic restart

---

### 2. Single-Step Config Files (Redundant)

- **data_loading.yaml**
- **filtering.yaml**
- **volcano.yaml**
- **go_enrich.yaml**
- **go_barplot.yaml**
- **go_analysis.yaml**
- **gene_clustering.yaml**
- **gene_filter_analysis.yaml**
- **GSEA_pipeline.yaml**

**Previous Usage:**
```bash
python src/analysis/filtering.py --config configs/filtering.yaml
```

**Why Redundant:**
- All scripts support `--config-section` parameter
- Can use main config file with section selection
- Reduces file duplication

**New Way (Use This):**
```bash
# Instead of separate filtering.yaml, use main config
python src/analysis/filtering.py \
  --config configs/GO_pipeline_H2O2.yaml \
  --config-section filtering \
  --in-csv input.csv \
  --out-csv output.csv
```

---

### 3. Backup Files (Old Config Format)

- **GO_pipeline_CHD8_backup.yaml**
- **GO_pipeline_Shank2_backup.yaml**

**Description:**
Original versions of main pipeline configs before refactoring to remove file paths (now managed by Snakemake).

**Changes Made:**
- Removed file path specifications (now in Snakemake rules)
- Simplified to only contain analysis parameters
- Separated standalone analysis configs (deg_comparison, gene_filter)

---

## 🔄 Migration Guide

### If You Need Batch Processing

**Old Way (Don't Use):**
```bash
python src/analysis/batch_runner.py --manifest configs/legacy/batch_manifest.yaml
```

**New Way (Use This):**
```bash
# For GO analysis
snakemake -s workflow/Snakefile_batch_GO \
  --configfile workflow/config/batch_go_config.yaml \
  -j 4

# For GSEA analysis
snakemake -s workflow/Snakefile_batch_GSEA \
  --configfile workflow/config/batch_gsea_config.yaml \
  -j 4
```

### If You Need Single Sample Analysis

**Use the simplified configs:**
```bash
# Copy appropriate config to workflow
cp configs/GO_pipeline_H2O2.yaml workflow/config/go_config.yaml

# Run Snakemake
snakemake -s workflow/Snakefile_GO \
  --configfile workflow/config/go_config.yaml
```

---

## 🗑️ Safe to Delete?

**Yes, if:**
- You have migrated to Snakemake workflows
- You don't need the old batch_runner.py script
- You have verified the new configs work for your use case

**Keep if:**
- You need to reference the old configuration structure
- You're in the middle of migration
- You want to compare old vs new approaches

---

## 📚 See Also

- **Current configs:** `../README.md`
- **Workflow documentation:** `../../workflow/README.md`
- **Migration guide:** `../../docs/MIGRATION_GUIDE.md`
