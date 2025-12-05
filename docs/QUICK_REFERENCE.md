# Snakemake Quick Reference Guide

## Essential Commands

### Dry Run (Always do this first!)
```bash
snakemake --snakefile Snakefile_batch_GO \
    --configfile configs/templates/batch_go_config.yaml \
    --dry-run --printshellcmds
```

### Execute Workflow
```bash
# Single core
snakemake --snakefile Snakefile_batch_GO \
    --configfile configs/templates/batch_go_config.yaml \
    --cores 1

# Multiple cores (parallel execution)
snakemake --snakefile Snakefile_batch_GO \
    --configfile configs/templates/batch_go_config.yaml \
    --cores 4
```

### Visualize Workflow
```bash
# Workflow DAG
snakemake --snakefile Snakefile_batch_GO \
    --configfile configs/templates/batch_go_config.yaml \
    --dag | dot -Tpng > dag.png

# Rule graph
snakemake --snakefile Snakefile_batch_GO \
    --configfile configs/templates/batch_go_config.yaml \
    --rulegraph | dot -Tpng > rulegraph.png
```

### Run Specific Rules
```bash
# Run up to a specific rule
snakemake --snakefile Snakefile_batch_GO \
    --configfile configs/templates/batch_go_config.yaml \
    --until filtering --cores 1

# Force re-run a specific rule
snakemake --snakefile Snakefile_batch_GO \
    --configfile configs/templates/batch_go_config.yaml \
    --forcerun go_enrich --cores 1
```

### Cluster Execution (SLURM)
```bash
snakemake --snakefile Snakefile_batch_GO \
    --configfile configs/templates/batch_go_config.yaml \
    --cluster "sbatch --time=02:00:00 --mem=16G --cpus-per-task=1" \
    --jobs 10
```

## Workflow Files

- `Snakefile_GO` - Single sample GO analysis
- `Snakefile_GSEA` - Single sample GSEA analysis
- `Snakefile_batch_GO` - Multi-sample batch GO analysis

## Configuration Files

- `configs/templates/go_config.yaml` - GO analysis config
- `configs/templates/gsea_config.yaml` - GSEA analysis config
- `configs/templates/batch_go_config.yaml` - Batch GO config
- `configs/templates/batch_go_config_template.yaml` - Template for new batch configs

## Common Options

- `--cores N` - Use N CPU cores
- `--cores all` - Use all available cores
- `--dry-run` - Show what would be done without executing
- `--printshellcmds` - Print shell commands being executed
- `--verbose` - Verbose output
- `--forceall` - Force re-execution of all rules
- `--forcerun RULE` - Force re-execution of specific rule
- `--until RULE` - Execute up to and including RULE
- `--cluster CMD` - Submit jobs to cluster
- `--jobs N` - Maximum number of cluster jobs

## Troubleshooting

### Check if files exist
```bash
snakemake --snakefile Snakefile_batch_GO \
    --configfile configs/templates/batch_go_config.yaml \
    --summary
```

### Clean up outputs (careful!)
```bash
# Remove all output files
snakemake --snakefile Snakefile_batch_GO \
    --configfile configs/templates/batch_go_config.yaml \
    --delete-all-output

# Remove specific rule outputs
snakemake --snakefile Snakefile_batch_GO \
    --configfile configs/templates/batch_go_config.yaml \
    --delete-output RULE
```

### View execution log
```bash
# Check logs in output directory
cat results/batch_go_snakemake/sample1/logs/*.log
```

## Performance Tips

1. **Use appropriate core count**: Match to your system or number of samples
2. **Start small**: Test with 1-2 samples before full batch
3. **Monitor resources**: Check memory and CPU usage
4. **Use cluster for large batches**: Submit to HPC for 10+ samples
5. **Check dry-run first**: Always verify execution plan

## Getting Help

```bash
# Snakemake help
snakemake --help

# Workflow-specific help
cat workflow/README.md

# Main documentation
cat README.md
```
