#!/bin/bash
# Quick start script for running Snakemake GSEA analysis
#
# Usage:
#   ./scripts/run_snakemake_gsea.sh configs/templates/gsea_config.yaml

set -e  # Exit on error

# Check if config file is provided
if [ $# -eq 0 ]; then
    echo "Error: No configuration file provided"
    echo "Usage: $0 <config_file>"
    echo ""
    echo "Example:"
    echo "  $0 configs/templates/gsea_config.yaml"
    exit 1
fi

CONFIG_FILE=$1
SNAKEFILE="Snakefile_GSEA"

# Verify config file exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Configuration file not found: $CONFIG_FILE"
    exit 1
fi

echo "Running GSEA analysis..."
echo "Configuration: $CONFIG_FILE"
echo "Snakefile: $SNAKEFILE"
echo ""

# Perform dry run first
echo "=== Performing dry run ==="
snakemake --snakefile "$SNAKEFILE" \
    --configfile "$CONFIG_FILE" \
    --dry-run \
    --printshellcmds

echo ""
echo "=== Dry run complete. Press Enter to continue with execution, or Ctrl+C to cancel ==="
read -r

# Execute the workflow
echo "=== Executing workflow ==="
snakemake --snakefile "$SNAKEFILE" \
    --configfile "$CONFIG_FILE" \
    --cores 2 \
    --printshellcmds

echo ""
echo "=== Workflow completed successfully ==="
