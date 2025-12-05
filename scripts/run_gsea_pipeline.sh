#!/bin/bash
# Convenience script to run complete GSEA pipeline
# Usage: ./scripts/run_gsea_pipeline.sh <config_file>

set -e  # Exit on error

if [ $# -eq 0 ]; then
    echo "Usage: $0 <config_file>"
    echo "Example: $0 configs/GSEA_pipeline.yaml"
    exit 1
fi

CONFIG_FILE="$1"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Configuration file '$CONFIG_FILE' not found"
    exit 1
fi

echo "=========================================="
echo "Running GSEA Pipeline"
echo "Configuration: $CONFIG_FILE"
echo "=========================================="
echo ""

# Determine Python executable
if command -v python &> /dev/null; then
    PYTHON=python
elif command -v python3 &> /dev/null; then
    PYTHON=python3
else
    echo "Error: Python not found"
    exit 1
fi

# Check if we're in the project root
if [ ! -d "src/analysis" ]; then
    echo "Error: Please run this script from the project root directory"
    exit 1
fi

echo "Step 1/3: Loading and preparing data..."
$PYTHON src/analysis/data_loading.py --config "$CONFIG_FILE" --config-section data_loading
echo "✓ Data loading complete"
echo ""

echo "Step 2/3: Running GSEA analysis..."
$PYTHON src/analysis/gsea_analysis.py --config "$CONFIG_FILE" --config-section gsea
echo "✓ GSEA analysis complete"
echo ""

echo "Step 3/3: Creating GSEA visualizations..."
$PYTHON src/analysis/gsea_plot.py --config "$CONFIG_FILE" --config-section gsea_plot
echo "✓ GSEA visualization complete"
echo ""

echo "=========================================="
echo "Pipeline complete! ✓"
echo "=========================================="
echo ""
echo "Check your output directory for results."
