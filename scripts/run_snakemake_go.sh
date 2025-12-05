#!/bin/bash
# Quick start script for running Snakemake GO analysis
#
# Usage:
#   ./scripts/run_snakemake_go.sh configs/templates/go_config.yaml
#   ./scripts/run_snakemake_go.sh configs/templates/batch_go_config.yaml --batch

set -e  # Exit on error

# Check if config file is provided
if [ $# -eq 0 ]; then
    echo "Error: No configuration file provided"
    echo "Usage: $0 <config_file> [--batch]"
    echo ""
    echo "Examples:"
    echo "  $0 configs/templates/go_config.yaml"
    echo "  $0 configs/templates/batch_go_config.yaml --batch"
    exit 1
fi

CONFIG_FILE=$1
BATCH_MODE=false

# Check for batch mode flag
if [ "$2" = "--batch" ]; then
    BATCH_MODE=true
fi

# Verify config file exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Configuration file not found: $CONFIG_FILE"
    exit 1
fi

# Select the appropriate Snakefile
if [ "$BATCH_MODE" = true ]; then
    SNAKEFILE="Snakefile_batch_GO"
    echo "Running batch GO analysis..."
else
    SNAKEFILE="Snakefile_GO"
    echo "Running single-sample GO analysis..."
fi

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
    --cores 4 \
    --printshellcmds

echo ""
echo "=== Workflow completed successfully ==="
