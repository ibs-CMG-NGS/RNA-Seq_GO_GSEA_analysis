# Migration Guide: New Installation and Workflow System

This document explains the changes made to the RNA-Seq GO/GSEA analysis pipeline installation and workflow execution system.

## Summary of Changes

### 1. Simplified Installation with Conda Environment

**Before**: Manual setup with clone → venv → requirements.txt → YG_utils_analysis
**After**: Single command conda environment creation

```bash
# Old method
git clone <repo>
cd RNA-Seq_GO_GSEA_analysis
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install git+https://github.com/parkgilbong/YG_utils_analysis.git@main
pip install -e .

# New method
git clone <repo>
cd RNA-Seq_GO_GSEA_analysis
conda env create -f environment.yml
conda activate rnaseq-analysis
```

**Benefits**:
- Single command installation
- Automatic dependency resolution
- Better reproducibility
- Easier to share and maintain

### 2. Snakemake Workflow Integration

**Before**: Sequential batch processing with Python script
**After**: Parallel workflow execution with Snakemake

**Why Snakemake?**
- **Parallel Execution**: Process multiple samples simultaneously
- **Dependency Tracking**: Only re-run what changed
- **Error Recovery**: Resume from failure points
- **Scalability**: Easy deployment to HPC clusters
- **Reproducibility**: Version-controlled workflow definitions

### 3. New Directory Structure

```
RNA-Seq_GO_GSEA_analysis/
├── environment.yml                    # NEW: Main conda environment
├── snakemake_environment.yml          # NEW: Snakemake-specific environment
├── workflow/                          # NEW: Snakemake workflow directory
│   ├── Snakefile_GO                  # NEW: GO analysis workflow
│   ├── Snakefile_GSEA                # NEW: GSEA analysis workflow
│   ├── Snakefile_batch_GO            # NEW: Batch GO workflow
│   ├── README.md                     # NEW: Workflow documentation
│   ├── QUICK_REFERENCE.md            # NEW: Quick reference guide
│   ├── config/                       # NEW: Workflow configurations
│   │   ├── go_config.yaml
│   │   ├── gsea_config.yaml
│   │   ├── batch_go_config.yaml
│   │   └── batch_go_config_template.yaml
│   └── scripts/                      # NEW: Helper scripts
│       ├── run_snakemake_go.sh
│       └── run_snakemake_gsea.sh
└── src/analysis/batch_runner.py       # KEPT: Python batch runner (alternative)
```

### 4. Workflow Execution Options

#### Option 1: Snakemake (Recommended for Batch Processing)

```bash
# Activate Snakemake environment
conda activate snakemake_env

# Run batch analysis
snakemake --snakefile workflow/Snakefile_batch_GO \
    --configfile workflow/config/batch_go_config.yaml \
    --cores 4
```

#### Option 2: Python Batch Runner (Alternative)

```bash
# Activate main environment
conda activate rnaseq-analysis

# Run batch analysis
python src/analysis/batch_runner.py --manifest configs/batch_manifest.yaml
```

#### Option 3: Interactive CLI (For Single Samples)

```bash
# Still available - no changes
python src/analysis/data_loading.py --config configs/GO_pipeline.yaml --config-section data_loading
python src/analysis/filtering.py --config configs/GO_pipeline.yaml --config-section filtering
# ... and so on
```

## Migration Steps for Existing Users

### Step 1: Update Your Repository

```bash
git pull origin main
```

### Step 2: Create New Conda Environment

```bash
# Remove old virtual environment if it exists
rm -rf venv/

# Create new conda environment
conda env create -f environment.yml
conda activate rnaseq-analysis
```

### Step 3: (Optional) Setup Snakemake Environment

```bash
# Only needed if you want to use Snakemake workflows
conda env create -f snakemake_environment.yml
```

### Step 4: Migrate Your Configurations

If you have custom batch manifest files:

1. Copy the template:
   ```bash
   cp workflow/config/batch_go_config_template.yaml workflow/config/my_batch.yaml
   ```

2. Edit `workflow/config/my_batch.yaml` with your sample information

3. Run with Snakemake:
   ```bash
   conda activate snakemake_env
   snakemake --snakefile workflow/Snakefile_batch_GO \
       --configfile workflow/config/my_batch.yaml \
       --cores 4
   ```

## Compatibility

### What Still Works

- All existing config files in `configs/` directory
- Python batch runner (`src/analysis/batch_runner.py`)
- Individual CLI tools
- Interactive notebooks
- Manual step-by-step execution

### What's New

- Conda environment files for easier setup
- Snakemake workflows for automated execution
- Parallel batch processing capabilities
- Workflow visualization with DAGs
- Helper scripts for common tasks

## Performance Comparison

### Sequential Processing (Python batch_runner.py)
- Processes samples one at a time
- Total time = Sum of all sample processing times
- Example: 4 samples × 30 min each = 120 minutes total

### Parallel Processing (Snakemake with --cores 4)
- Processes up to 4 samples simultaneously
- Total time ≈ Max sample processing time + overhead
- Example: 4 samples × 30 min each = ~35 minutes total (with 4 cores)

**Speed Improvement**: 3-4x faster for batch processing on multi-core systems

## Troubleshooting

### Issue: Conda environment creation fails

**Solution**: Update conda and try again
```bash
conda update -n base -c defaults conda
conda env create -f environment.yml
```

### Issue: Snakemake not found

**Solution**: Make sure you're in the correct environment
```bash
conda activate snakemake_env
snakemake --version
```

### Issue: Missing input files in Snakemake

**Solution**: Check paths in config file - they should be relative to project root
```bash
# Run dry-run to see what files Snakemake expects
snakemake --snakefile workflow/Snakefile_batch_GO \
    --configfile workflow/config/batch_go_config.yaml \
    --dry-run
```

## Resources

- **Main README**: `README.md` - Complete documentation
- **Workflow README**: `workflow/README.md` - Snakemake workflow details
- **Quick Reference**: `workflow/QUICK_REFERENCE.md` - Common Snakemake commands
- **Config Template**: `workflow/config/batch_go_config_template.yaml` - Example configuration

## Getting Help

1. Check the documentation files listed above
2. Run Snakemake dry-run to preview execution
3. Review log files in output directories
4. Open an issue on GitHub with details

## Summary

This update modernizes the pipeline with industry-standard workflow management while maintaining backward compatibility. Existing scripts and workflows continue to work, and you can adopt the new Snakemake workflows at your own pace.

**Key Takeaways**:
- ✅ Installation is now simpler with conda environments
- ✅ Batch processing is faster with Snakemake parallelization
- ✅ All existing functionality is preserved
- ✅ New workflows are optional but recommended
- ✅ Better suited for HPC and large-scale analyses
