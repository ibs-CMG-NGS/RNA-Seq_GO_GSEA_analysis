# =================================
# file: src/analysis/compare_degs.py
# =================================
# This module provides functionality to compare two lists of differentially expressed genes (DEGs).
# It generates a Venn diagram to visualize the overlap between the two gene sets and a heatmap
# to compare the log2 fold change values of the common genes.
# The script is configurable via a YAML file and command-line arguments.
#
# Functions
# ---------
# - compare_and_visualize_degs(path1: str, path2: str, name1: str, name2: str, ...) -> None:
#     Compares two DEG files, generates a Venn diagram of overlapping genes, and creates a heatmap of log2FC values for the overlapping genes.
# - _parse_args(argv=None) -> argparse.Namespace:
#     Parses command-line arguments for configuration file and section.
# - _main(argv=None) -> None:
#     The main entry point for the command-line script. It loads configuration and data, then orchestrates the comparison and visualization.
#
# Usage
# -----
# Run as a script to compare two DEG files using a configuration file:
#     python compare_degs.py --config configs/GO_pipeline.yaml --config-section deg_comparison
#
# Dependencies
# ------------
# - pandas, matplotlib, seaborn, argparse, logging
# - matplotlib_venn (optional)
# - utils.FileFunctions, utils.config_utils

import argparse
import logging

from pathlib import Path
from typing import Optional, Tuple

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from utils.FileFunctions import ensure_dir
from utils.config_utils import get_cfg, pick, resolve_path

# Optional dependency for Venn diagrams
try:
    from matplotlib_venn import venn2
    _VENN = True
except ImportError:
    _VENN = False
    logging.warning("matplotlib-venn is not installed. Venn diagram plotting will be skipped.")


def compare_and_visualize_degs(
    path1: str,
    path2: str,
    name1: str,
    name2: str,
    out_venn_png: str,
    out_heatmap_png: str,
    log2fc_col: str = "log2fc",
    gene_col: str = "gene",
    heatmap_top_n: Optional[int] = 50,
    heatmap_cmap: str = "RdBu_r",
    heatmap_annot_kws: Optional[dict] = None,
    venn_colors: Optional[Tuple[str, str]] = ("#1f77b4", "#ff7f0e"),
    venn_alpha: float = 0.6,
):
    """
    Compares two DEG files, generates a Venn diagram of overlapping genes,
    and creates a heatmap of log2FC values for the overlapping genes.
    """
    df1 = pd.read_csv(path1)
    df2 = pd.read_csv(path2)

    # The input files are assumed to be pre-filtered DEG lists.
    genes1 = set(df1[gene_col].dropna())
    genes2 = set(df2[gene_col].dropna())

    logging.info(f"Number of DEGs in {name1}: {len(genes1)}")
    logging.info(f"Number of DEGs in {name2}: {len(genes2)}")

    # 1. Venn Diagram
    if _VENN and out_venn_png:
        plt.figure(figsize=(6, 6))
        venn2(
            [genes1, genes2],
            set_labels=(name1, name2),
            set_colors=venn_colors or ("r", "g"),
            alpha=venn_alpha
        )
        plt.title("Overlap of Differentially Expressed Genes (DEGs)")
        ensure_dir(Path(out_venn_png).parent)
        plt.savefig(out_venn_png, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Saved Venn diagram: {out_venn_png}")

    # 2. Heatmap for overlapping genes
    overlap_genes = genes1.intersection(genes2)
    logging.info(f"Number of overlapping DEGs: {len(overlap_genes)}")

    if out_heatmap_png:
        if not overlap_genes:
            print("No overlapping DEGs found. Skipping heatmap generation.")
            return

        # Extract log2FC values for overlapping genes
        overlap1 = df1[df1[gene_col].isin(overlap_genes)][[gene_col, log2fc_col]].set_index(gene_col)
        overlap2 = df2[df2[gene_col].isin(overlap_genes)][[gene_col, log2fc_col]].set_index(gene_col)

        # Combine data and sort for better visualization
        combined_data = pd.DataFrame({
            name1: overlap1[log2fc_col],
            name2: overlap2[log2fc_col]
        }).fillna(0)

        # Sort to get top up-regulated and top down-regulated genes
        sorted_up = combined_data.sort_values(name1, ascending=False)
        sorted_down = combined_data.sort_values(name1, ascending=True)

        # Select top N from each group if specified
        if heatmap_top_n:
            top_genes = sorted_up.head(heatmap_top_n)
            bottom_genes = sorted_down.head(heatmap_top_n)
            plot_data = pd.concat([top_genes, bottom_genes]).drop_duplicates()
            title = f'Top {heatmap_top_n} Up & Down Overlapping DEGs'
        else:
            # If top_n is not set, plot all overlapping genes, sorted by log2FC
            plot_data = sorted_up
            title = f'Log2 Fold Change of Overlapping DEGs ({len(plot_data)})'
        
        plot_data = plot_data.sort_values(name1, ascending=False)

        # Create Heatmap
        plt.figure(figsize=(8, min(25, len(plot_data) * 0.4 + 2)))
        sns.heatmap(
            plot_data,
            cmap=heatmap_cmap,
            center=0,
            annot=plot_data if heatmap_top_n else False,
            fmt='.2f',
            annot_kws=heatmap_annot_kws or {"size": 8},
            linewidths=.5,
            xticklabels=True,
            yticklabels=True
        )
        plt.title(title)
        plt.tight_layout()
        ensure_dir(Path(out_heatmap_png).parent)
        plt.savefig(out_heatmap_png, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Saved heatmap of overlapping DEGs: {out_heatmap_png}")


def _parse_args(argv=None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Compare two DEG lists, create Venn diagram and heatmap.")
    p.add_argument("--config", required=True, help="Path to the pipeline YAML configuration file.")
    p.add_argument("--config-section", default="deg_comparison", help="Section name in the YAML file.")
    # CLI arguments can override config file settings
    p.add_argument("--file1", help="Path to the first DEG file.")
    p.add_argument("--file2", help="Path to the second DEG file.")
    p.add_argument("--name1", help="Name for the first dataset (e.g., 'KD_vs_Scr').")
    p.add_argument("--name2", help="Name for the second dataset (e.g., 'OE_vs_Scr').")
    p.add_argument("--out-venn-png", help="Output path for the Venn diagram PNG.")
    p.add_argument("--out-heatmap-png", help="Output path for the heatmap PNG.")
    return p.parse_args(argv)


def _main(argv=None) -> None:
    args = _parse_args(argv)
    cfg_all = get_cfg(args.config)
    cfg_section = cfg_all.get(args.config_section, {})

    # --- Resolve all paths consistently ---
    # Helper to resolve a single optional path.
    # These are intermediate files, relative to ROOT_DIR (is_input=False).
    def _resolve_single_path(arg_val, key):
        paths = resolve_path(
            cli_path=[arg_val] if arg_val else None,
            cfg=cfg_all, config_key=key, config_section=args.config_section
        )
        return paths[0] if paths else None

    file1 = _resolve_single_path(args.file1, "file1")
    file2 = _resolve_single_path(args.file2, "file2")
    out_venn_png = _resolve_single_path(args.out_venn_png, "out_venn_png")
    out_heatmap_png = _resolve_single_path(args.out_heatmap_png, "out_heatmap_png")

    # Input files are required for comparison
    if not (file1 and file2 and Path(file1).exists() and Path(file2).exists()):
        raise SystemExit(f"Both input files must be specified and exist. Got: {file1}, {file2}")

    # Pick non-path parameters
    name1 = pick(args.name1, cfg_section, "name1", "Set 1")
    name2 = pick(args.name2, cfg_section, "name2", "Set 2")
    log2fc_col = pick(None, cfg_section, "log2fc_col", "log2fc")
    gene_col = pick(None, cfg_section, "gene_col", "gene")

    # Styling options from config
    heatmap_top_n = pick(None, cfg_section, "heatmap_top_n", 50)
    heatmap_cmap = pick(None, cfg_section, "heatmap_cmap", "RdBu_r")
    heatmap_annot_kws = pick(None, cfg_section, "heatmap_annot_kws", {"size": 8})
    venn_colors = pick(None, cfg_section, "venn_colors", ("#1f77b4", "#ff7f0e"))
    venn_alpha = pick(None, cfg_section, "venn_alpha", 0.6)

    compare_and_visualize_degs(
        path1=file1,
        path2=file2,
        name1=name1,
        name2=name2,
        out_venn_png=out_venn_png, # Can be None
        out_heatmap_png=out_heatmap_png, # Can be None
        log2fc_col=log2fc_col,
        gene_col=gene_col,
        heatmap_top_n=int(heatmap_top_n) if heatmap_top_n else None,
        heatmap_cmap=heatmap_cmap,
        heatmap_annot_kws=heatmap_annot_kws,
        venn_colors=tuple(venn_colors) if isinstance(venn_colors, list) else venn_colors,
        venn_alpha=float(venn_alpha),
    )


if __name__ == "__main__":
    _main()
