#!/bin/bash
# Convenience script to run complete GO enrichment pipeline
# Usage: ./scripts/run_go_pipeline.sh <config_file>

set -e  # Exit on error

if [ $# -eq 0 ]; then
    echo "Usage: $0 <config_file>"
    echo "Example: $0 configs/GO_pipeline_Shank2.yaml"
    exit 1
fi

CONFIG_FILE="$1"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Configuration file '$CONFIG_FILE' not found"
    exit 1
fi

echo "=========================================="
echo "Running GO Enrichment Pipeline"
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

echo "Step 1/6: Loading and standardizing data..."
$PYTHON src/analysis/data_loading.py --config "$CONFIG_FILE" --config-section data_loading
echo "✓ Data loading complete"
echo ""

echo "Step 2/6: Filtering significant DEGs..."
$PYTHON src/analysis/filtering.py --config "$CONFIG_FILE" --config-section filtering
echo "✓ Filtering complete"
echo ""

echo "Step 3/6: Generating volcano plot..."
$PYTHON src/analysis/volcano.py --config "$CONFIG_FILE" --config-section volcano
echo "✓ Volcano plot generated"
echo ""

echo "Step 4/6: Running GO enrichment analysis..."
$PYTHON src/analysis/go_enrich.py --config "$CONFIG_FILE" --config-section go_enrich
echo "✓ GO enrichment complete"
echo ""

echo "Step 5/6: Creating GO visualization..."
$PYTHON src/analysis/go_barplot.py --config "$CONFIG_FILE" --config-section go_barplot
echo "✓ GO visualization complete"
echo ""

echo "Step 6/6: Generating final report..."
$PYTHON src/analysis/report_generation.py --config "$CONFIG_FILE" --config-section report
echo "✓ Report generated"
echo ""

echo "=========================================="
echo "Pipeline complete! ✓"
echo "=========================================="
echo ""
echo "Check your output directory for results."
