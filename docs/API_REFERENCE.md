# API Reference

This document provides a comprehensive reference for the Python API of the RNA-Seq GO/GSEA analysis pipeline. Use this when you want to programmatically use the analysis functions in your own scripts or notebooks.

## Core Utility Modules

### `src/utils.py` - Core Utilities

General-purpose utility functions used across the pipeline.

#### `ensure_outdir(path: str) -> str`

Create a directory if it doesn't exist.

**Parameters:**
- `path` (str): Directory path to create

**Returns:**
- str: The same path (for chaining)

**Example:**
```python
from utils import ensure_outdir
output_dir = ensure_outdir("results/analysis1")
```

#### `load_genes(path: str, inline_genes: Optional[List[str]] = None) -> List[str]`

Load gene symbols from a file or inline list, removing duplicates.

**Parameters:**
- `path` (str): Path to a text file with one gene per line
- `inline_genes` (Optional[List[str]]): Optional list of genes to use instead of reading from file

**Returns:**
- List[str]: List of unique gene symbols in order of first appearance

**Example:**
```python
from utils import load_genes

# Load from file
genes = load_genes("genes_of_interest.txt")

# Or provide directly
genes = load_genes("", inline_genes=["BRCA1", "TP53", "BRCA1"])
print(len(genes))  # 2 (duplicates removed)
```

#### `filter_genes_by_thresholds(...) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, List[str]]`

Filter genes based on statistical significance and fold change thresholds.

**Parameters:**
- `df` (pd.DataFrame): DataFrame containing gene expression data
- `gene_col` (str): Name of column containing gene symbols
- `padj_col` (str): Name of column containing adjusted p-values
- `log2fc_col` (str): Name of column containing log2 fold changes
- `adj_p_cutoff` (float): Adjusted p-value threshold (e.g., 0.05)
- `log2fc_cutoff` (float): Absolute log2 fold change threshold (e.g., 1.0)
- `direction` (str): Filter direction - "up", "down", or "both"

**Returns:**
- Tuple of (filtered_df, up_regulated_df, down_regulated_df, gene_list)

**Example:**
```python
from utils import filter_genes_by_thresholds
import pandas as pd

df = pd.DataFrame({
    "gene": ["A", "B", "C"],
    "log2fc": [2.0, -1.5, 0.5],
    "padj": [0.001, 0.01, 0.1]
})

filt, up, down, genes = filter_genes_by_thresholds(
    df, "gene", "padj", "log2fc", 0.05, 1.0, "both"
)
print(f"Found {len(genes)} significant genes")
```

#### Visualization Functions

See module docstrings for `barplot()`, `dotplot()`, and `volcano_plot()` functions.

### `src/io_utils.py` - I/O Utilities

Simple wrapper functions for file I/O operations.

### `src/filter_utils.py` - Filtering Utilities  

Functions for filtering gene expression data based on gene lists.

### `src/viz_utils.py` - Visualization Utilities

Publication-quality plotting functions for heatmaps and dot plots.

## Analysis Modules

### `src/analysis/data_loading.py`

Functions for loading and standardizing gene expression data from Excel files.

Key function: `load_excels(raw_excels, sheets, column_map)` - Load and standardize multiple Excel files

### `src/analysis/filtering.py`

Functions for filtering differentially expressed genes by statistical thresholds.

Key functions:
- `filter_by_thresholds()` - Filter by p-value and fold change
- `filter_by_gene_list()` - Filter by predefined gene list

### `src/analysis/volcano.py`

Create volcano plots for differential expression visualization.

Key function: `plot_volcano()` - Generate volcano plot with customizable styling

### `src/analysis/go_enrich.py`

Perform GO enrichment analysis using GOATOOLS.

Key function: `run_go_enrichment()` - Run GO enrichment with specified parameters

### `src/analysis/gsea_analysis.py`

Run Gene Set Enrichment Analysis using GSEApy.

Key functions:
- `run_gsea_prerank()` - Pre-ranked GSEA
- `run_gsea_classic()` - Classic GSEA with expression matrix

## Using the API in Your Own Scripts

### Example: Custom Analysis Script

```python
#!/usr/bin/env python
"""Custom analysis combining pipeline functions."""
import pandas as pd
from pathlib import Path
from analysis.data_loading import load_excels
from analysis.filtering import filter_by_thresholds
from analysis.volcano import plot_volcano
from utils import ensure_outdir

def my_custom_analysis(input_file: str, output_dir: str):
    """Run a custom RNA-Seq analysis workflow."""
    output_dir = Path(output_dir)
    ensure_outdir(str(output_dir))
    
    # Load data
    column_map = {"gene": "Gene Symbol", "log2fc": "log2FC", "padj": "adjusted p-value"}
    df = load_excels([input_file], sheets=["Results"], column_map=column_map)
    
    # Filter for significant genes
    sig_genes = filter_by_thresholds(
        df, padj_col="padj", log2fc_col="log2fc",
        padj_cutoff=0.01, log2fc_cutoff=1.5, direction="both"
    )
    
    # Save results
    sig_genes.to_csv(output_dir / "significant_genes.csv", index=False)
    
    # Create volcano plot
    plot_volcano(df, str(output_dir / "volcano.png"), 0.01, 1.5)
    
    print(f"Found {len(sig_genes)} significant genes.")
    return sig_genes

if __name__ == "__main__":
    my_custom_analysis("data/input.xlsx", "output/custom")
```

### Example: Batch Processing with Custom Logic

```python
"""Process multiple samples with custom filtering."""
import pandas as pd
from pathlib import Path
from analysis.data_loading import load_excels
from analysis.filtering import filter_by_thresholds

def process_sample(sample_name: str, input_file: str, output_dir: Path):
    """Process a single sample."""
    column_map = {"gene": "Gene", "log2fc": "logFC", "padj": "FDR"}
    df = load_excels([input_file], None, column_map)
    
    significant = filter_by_thresholds(
        df, "padj", "log2fc", 0.05, 1.0, "both"
    )
    
    output_file = output_dir / f"{sample_name}_significant.csv"
    significant.to_csv(output_file, index=False)
    return len(significant)

# Process multiple samples
samples = {
    "sample1": "data/sample1.xlsx",
    "sample2": "data/sample2.xlsx",
}

output = Path("output/batch")
output.mkdir(parents=True, exist_ok=True)

results = {name: process_sample(name, file, output) 
           for name, file in samples.items()}

# Create summary
summary = pd.DataFrame([
    {"Sample": name, "Significant_Genes": count}
    for name, count in results.items()
])
summary.to_csv(output / "summary.csv", index=False)
```

## Configuration Utilities

The `utils.config_utils` module (from YG_utils_analysis) provides:

- `get_cfg(config_path)` - Load YAML configuration
- `resolve_path(...)` - Resolve file paths relative to project root
- `pick(cli_arg, config, key, default)` - Prioritize CLI args over config

## Best Practices

1. **Use Path objects** for file operations
2. **Add type hints** to your functions
3. **Leverage configuration utilities** instead of hardcoding
4. **Handle errors gracefully** with try/except
5. **Use logging** instead of print statements

## Further Documentation

- See module docstrings for complete function signatures
- Check README.md for CLI usage
- Review notebooks for interactive examples
- Read CONTRIBUTING.md for development guidelines

For questions, open an issue on GitHub.
