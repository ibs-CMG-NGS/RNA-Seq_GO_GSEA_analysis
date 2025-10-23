# src/analysis/gene_filter_analysis.py
# ============================================
# file: src/analysis/gene_filter_analysis.py
# ============================================
# This module provides functionality to filter gene expression data from multiple standardized CSV files based on a specific gene list.
# It generates a comparative dot plot visualizing the log2 fold change and adjusted p-values of the selected genes across different datasets.
# The script is configurable via a YAML file and command-line arguments.
#
# Functions
# ---------
# - run_gene_filter_analysis(input_csvs: List[Path], file_aliases: List[str], gene_list: List[str], ...) -> pd.DataFrame:
#     Filters data from multiple CSVs for a given gene list, combines the results, and generates a comparative dot plot.
# - _parse_args(argv=None) -> argparse.Namespace:
#     Parses command-line arguments for input files, gene list, column mapping, and output directory.
# - _main(argv=None) -> None:
#     The main entry point for the command-line script. It loads configuration and data, then orchestrates the analysis and visualization.
#
# Usage
# -----
# Run as a script to filter and visualize genes from multiple datasets using a configuration file:
#     python gene_filter_analysis.py --config configs/GO_pipeline.yaml --config-section gene_filter
#
# Dependencies
# ------------
# - pandas, matplotlib, argparse
# - src.filter_utils, src.viz_utils, utils.config_utils, utils.FileFunctions, utils.OmicsFunctions

import sys

import argparse
import logging
from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
from src.filter_utils import filter_genes
from src.viz_utils import plot_dot_plot
from utils.config_utils import get_cfg, pick, resolve_path
from utils.FileFunctions import ensure_dir
from utils.OmicsFunctions import read_gene_list

def run_gene_filter_analysis(
    input_csvs: List[Path],
    file_aliases: List[str],
    gene_list: List[str],
    col_map: Dict[str, str],
    plot_options: Dict,
    output_dir: Path,
    pdf: Optional[PdfPages] = None
) -> pd.DataFrame:
    """Filters data from multiple datasets based on a gene list, saves a Dot Plot and a combined results CSV."""
    all_filtered_dfs = []
    gene_col, log2fc_col, padj_col = col_map["gene"], col_map["log2fc"], col_map["padj"]

    for i, csv_path in enumerate(input_csvs):
        alias = file_aliases[i] if i < len(file_aliases) else csv_path.stem
        df = pd.read_csv(csv_path)
        filtered = filter_genes(df, gene_list, gene_col=gene_col)
        if not filtered.empty:
            # Record the origin of each dataset in the 'source' column using its alias
            filtered['source'] = alias
            all_filtered_dfs.append(filtered)

    if not all_filtered_dfs:
        logging.warning("The genes of interest were not found in any of the datasets.")
        return pd.DataFrame()

    # Combine all filtered data into a single DataFrame
    combined_df = pd.concat(all_filtered_dfs, ignore_index=True)
    combined_df.to_csv(output_dir / "filtered_genes_combined.csv", index=False)

    # Restructure data for the Dot Plot
    pivot_log2fc = combined_df.pivot_table(index=gene_col, columns='source', values=log2fc_col)
    pivot_pval = combined_df.pivot_table(index=gene_col, columns='source', values=padj_col)
    plot_dot_plot(pivot_log2fc, pivot_pval, "Gene Expression Dot Plot", plot_options, output_dir / "dotplot_comparison.png", pdf, gene_order=gene_list)
    
    return combined_df

def _parse_args(argv=None) -> argparse.Namespace:
    """Parses CLI arguments."""
    p = argparse.ArgumentParser(description="Filter data based on a gene list and generate a comparative dot plot.")
    p.add_argument("--config", help="Path to the YAML configuration file.")
    p.add_argument("--config-section", default="gene_filter", help="Section name within the YAML file.")
    p.add_argument("--in-csv-files", nargs='+', help="List of standardized CSV files to analyze.")
    p.add_argument("--gene-list-file", help="Path to the text file containing the list of genes to analyze.")
    p.add_argument("--gene-col", help="Column name for gene symbols.")
    p.add_argument("--log2fc-col", help="Column name for Log2 Fold Change values.")
    p.add_argument("--padj-col", help="Column name for adjusted p-values.")
    p.add_argument("--output-dir", help="Directory to save the results.")
    return p.parse_args(argv)

def _main(argv=None) -> None:
    """Main entry point for the CLI script."""
    args = _parse_args(argv)
    cfg_all = get_cfg(args.config) or {}
    cfg = cfg_all.get(args.config_section, {})
    plot_options = cfg.get("plot_options", {})
    cfg_cols = cfg.get("column_map", {})

    # Resolve all paths consistently
    input_csv_paths = resolve_path(
        cli_path=args.in_csv_files,
        cfg=cfg_all, config_key="in_csv_files", config_section=args.config_section,
        is_input=True # These are input files relative to the project root
    )
    
    output_dir_paths = resolve_path(
        cli_path=[args.output_dir] if args.output_dir else None,
        cfg=cfg_all, config_key="output_dir", config_section=args.config_section
    )
    output_dir = output_dir_paths[0] if output_dir_paths else None

    gene_list_paths = resolve_path(
        cli_path=[args.gene_list_file] if args.gene_list_file else None,
        cfg=cfg_all, config_key="gene_list_file", config_section=args.config_section,
        is_input=True # This is an input file relative to the project root
    )
    gene_list_file = gene_list_paths[0] if gene_list_paths else None

    # Pick non-path parameters
    file_aliases = cfg.get("file_aliases", [])
    col_map = {
        "gene": pick(args.gene_col, cfg_cols, "gene"),
        "log2fc": pick(args.log2fc_col, cfg_cols, "log2fc"),
        "padj": pick(args.padj_col, cfg_cols, "padj"),
    }

    if not all([input_csv_paths, output_dir, gene_list_file]):
        raise SystemExit("Missing required settings: in_csv_files, output_dir, and gene_list_file must be provided.")

    gene_list = read_gene_list(gene_list_file)
    if not gene_list:
        logging.warning("Gene list is empty. Skipping analysis.")
        return

    # Create output directory
    ensure_dir(output_dir)

    # Prepare PDF file for plots
    pdf_path = Path(output_dir) / "gene_filter_dotplots.pdf"
    with PdfPages(pdf_path) as pdf:
        run_gene_filter_analysis(
            input_csvs=[Path(p) for p in input_csv_paths],
            file_aliases=file_aliases,
            gene_list=gene_list,
            col_map=col_map,
            plot_options=plot_options,
            output_dir=Path(output_dir),
            pdf=pdf
        )
    
    print(f"Analysis complete. Results saved to: {output_dir}")


if __name__ == "__main__":
    _main()
