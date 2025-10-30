# Snakemake Workflows for RNA-Seq Analysis

This directory contains Snakemake workflow files for automating RNA-Seq post-analysis pipelines.

## Workflow Files

### Single Sample Workflows

- **Snakefile_GO**: Gene Ontology enrichment analysis pipeline for a single sample
- **Snakefile_GSEA**: Gene Set Enrichment Analysis pipeline for a single sample

### Batch Processing Workflow

- **Snakefile_batch_GO**: Batch processing of multiple samples through the GO enrichment pipeline

## Configuration Files

Configuration files are located in `workflow/config/`:

- `go_config.yaml`: Configuration for single-sample GO analysis
- `gsea_config.yaml`: Configuration for single-sample GSEA analysis
- `batch_go_config.yaml`: Configuration for batch GO analysis with multiple samples

## Quick Start

### Run GO Analysis (Single Sample)

```bash
# Activate Snakemake environment
conda activate snakemake_env

# Run the GO pipeline
snakemake --snakefile workflow/Snakefile_GO --configfile workflow/config/go_config.yaml --cores 1
```

### Run GSEA Analysis (Single Sample)

```bash
# Run the GSEA pipeline
snakemake --snakefile workflow/Snakefile_GSEA --configfile workflow/config/gsea_config.yaml --cores 1
```

### Run Batch GO Analysis (Multiple Samples)

```bash
# Run batch processing for all samples defined in batch_go_config.yaml
snakemake --snakefile workflow/Snakefile_batch_GO --configfile workflow/config/batch_go_config.yaml --cores 4
```

## Workflow Visualization

You can visualize the workflow DAG (Directed Acyclic Graph):

```bash
# Generate workflow diagram
snakemake --snakefile workflow/Snakefile_GO --configfile workflow/config/go_config.yaml --dag | dot -Tpng > dag.png

# Generate rule graph
snakemake --snakefile workflow/Snakefile_GO --configfile workflow/config/go_config.yaml --rulegraph | dot -Tpng > rulegraph.png
```

## Dry Run

Before running the actual analysis, you can perform a dry run to see what would be executed:

```bash
snakemake --snakefile workflow/Snakefile_GO --configfile workflow/config/go_config.yaml --dry-run
```

## Parallel Execution

Snakemake can execute independent tasks in parallel. Use the `--cores` parameter:

```bash
# Use 4 CPU cores
snakemake --snakefile workflow/Snakefile_batch_GO --configfile workflow/config/batch_go_config.yaml --cores 4

# Use all available cores
snakemake --snakefile workflow/Snakefile_batch_GO --configfile workflow/config/batch_go_config.yaml --cores all
```

## Cluster Execution

For HPC clusters with SLURM:

```bash
snakemake --snakefile workflow/Snakefile_batch_GO \
    --configfile workflow/config/batch_go_config.yaml \
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
