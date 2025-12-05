# ================================
# Module: filtering.py
#=================================
# This module provides functions and a command-line interface for filtering RNA-Seq differential expression results.
# It supports filtering by statistical thresholds (adjusted p-value and log2 fold change) and by gene lists.
# Functions:
# ----------
# filter_by_thresholds(df: pd.DataFrame, padj_cutoff: float, log2fc_cutoff: float, direction: str = "both") -> pd.DataFrame
# filter_by_gene_list(df: pd.DataFrame, genes: Set[str]) -> pd.DataFrame
# _main(argv=None) -> None
#     Main CLI entry point. Parses arguments and applies filtering to an input CSV file, saving the result.
# Usage:
# ------
# Run as a script to filter a standardized CSV file by thresholds or gene list, using command-line arguments or a YAML config.
# Example:
# --------
# python filtering.py --in-csv input.csv --out-csv filtered.csv --mode thresholds --padj-cutoff 0.05 --log2fc-cutoff 1.0 --direction both
# Dependencies:
# -------------
# - pandas
# - argparse
# - logging
# - pathlib
# - utils.FileFunctions
# - utils.OmicsFunctions
# - utils.config_utils
# file: src/analysis/filtering.py
# ================================
import argparse
import logging
from pathlib import Path
from typing import Set
import pandas as pd

from utils.FileFunctions import ensure_dir 
from utils.OmicsFunctions import load_genes
from utils.config_utils import get_cfg, pick, resolve_path
from utils.logging_utils_environ import setup_logging

# This function intelligently finds the log file set by the notebook.
logging, _ = setup_logging()

def filter_by_thresholds(
    df: pd.DataFrame,
    padj_col: str,
    log2fc_col: str,
    padj_cutoff: float,
    log2fc_cutoff: float,
    direction: str = "both",
) -> pd.DataFrame:
    """
    Filters a DataFrame of differential expression results based on significance and fold change thresholds.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        padj_col (str): Name of the column containing adjusted p-values.
        log2fc_col (str): Name of the column containing log2 fold changes.
        padj_cutoff (float): Adjusted p-value threshold for significance.
        log2fc_cutoff (float): Log2 fold change threshold for filtering.
        direction (str, optional): Direction of fold change to filter by.
            - "up": Selects rows with log2fc >= abs(log2fc_cutoff).
            - "down": Selects rows with log2fc <= -abs(log2fc_cutoff).
            - "both" (default): Selects rows with absolute log2fc >= abs(log2fc_cutoff).

    Returns:
        pd.DataFrame: Filtered DataFrame containing rows that meet the specified thresholds.
    """
    direction = direction.lower()
    sig = df[padj_col] < padj_cutoff
    fc_abs = abs(log2fc_cutoff)
    fc = (
        (df[log2fc_col] >= fc_abs) if direction == "up" else
        (df[log2fc_col] <= -fc_abs) if direction == "down" else
        (df[log2fc_col].abs() >= fc_abs)
    )
    out = df.loc[sig & fc].copy()
    logging.info("Filtered(thresholds): n=%d", len(out))
    return out


def filter_by_gene_list(df: pd.DataFrame, genes: Set[str]) -> pd.DataFrame:
    """
    Filters the input DataFrame to include only rows where the 'gene' column matches any gene in the provided set.

    Args:
        df (pd.DataFrame): Input DataFrame containing gene data with a 'gene' column.
        genes (Set[str]): Set of gene names to filter by.

    Returns:
        pd.DataFrame: A new DataFrame containing only rows with genes present in the provided set.
    """
    out = df[df["gene"].isin(genes)].copy()
    logging.info("Filtered(gene_list): n=%d", len(out))
    return out


# -------- CLI: standardized CSV -> filtered CSV --------

def _parse_args(argv=None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Filter standardized CSV by thresholds or gene list")
    p.add_argument("--config", default=None, help="pipeline.yaml or filtering.yaml")
    p.add_argument("--config-section", default="filtering", help="YAML section name")
    p.add_argument("--in-csv", default=None)
    p.add_argument("--mode", choices=["thresholds", "gene_list"], default=None)
    p.add_argument("--padj-col", default=None, help="Name of the adjusted p-value column")
    p.add_argument("--log2fc-col", default=None, help="Name of the log2FC column")
    p.add_argument("--padj-cutoff", type=float, default=None)
    p.add_argument("--log2fc-cutoff", type=float, default=None)
    p.add_argument("--direction", choices=["up", "down", "both"], default=None)
    p.add_argument("--gene-list", default=None)
    p.add_argument("--out-up-genes", default=None, help="Path to save up-regulated gene list")
    p.add_argument("--out-down-genes", default=None, help="Path to save down-regulated gene list")
    p.add_argument("--out-csv", default=None)
    return p.parse_args(argv)


def _main(argv=None) -> None:
    args = _parse_args(argv)
    cfg_all = get_cfg(args.config) or {}
    cfg_section = cfg_all.get(args.config_section, cfg_all)

    # --- File paths from CLI (required for Snakemake) ---
    if not args.in_csv or not args.out_csv:
        raise SystemExit("Error: --in-csv and --out-csv are required when running via Snakemake")
    
    in_csv = args.in_csv
    out_csv = args.out_csv

    # --- Analysis parameters from config or CLI ---
    mode = pick(args.mode, cfg_section, "mode", default="thresholds")
    padj_col = pick(args.padj_col, cfg_section, "padj_col", default="padj")
    log2fc_col = pick(args.log2fc_col, cfg_section, "log2fc_col", default="log2fc")
    padj_cutoff = pick(args.padj_cutoff, cfg_section, "padj_cutoff", default=0.05)
    log2fc_cutoff = pick(args.log2fc_cutoff, cfg_section, "log2fc_cutoff", default=0)
    direction = pick(args.direction, cfg_section, "direction", default="both")

    # Optional gene list file path (for gene_list mode)
    gene_list_file = None
    if args.gene_list:
        gene_list_file = args.gene_list
    elif mode == "gene_list":
        # Try to get from config (project-root-relative)
        gene_list_paths = resolve_path(
            cli_path=None,
            cfg=cfg_all, 
            config_key="gene_list_file", 
            config_section=args.config_section,
            is_input=True
        )
        gene_list_file = gene_list_paths[0] if gene_list_paths else None

    # --- Perform filtering ---
    df = pd.read_csv(in_csv)
    
    if mode == "gene_list":
        if not gene_list_file:
            raise SystemExit("gene_list mode requires --gene-list or config.gene_list_file")
        genes = load_genes(gene_list_file)
        out = filter_by_gene_list(df, genes)
    else:
        out = filter_by_thresholds(df, padj_col, log2fc_col, padj_cutoff, log2fc_cutoff, direction)

    # Save filtered results
    ensure_dir(Path(out_csv).parent)
    out.to_csv(out_csv, index=False)
    logging.info(f"Saved filtered CSV: {out_csv}")

    # --- Save up/down gene lists if in thresholds mode ---
    if mode == "thresholds":
        up_genes = out[out[log2fc_col] > 0]["gene"].dropna().astype(str).unique()
        down_genes = out[out[log2fc_col] < 0]["gene"].dropna().astype(str).unique()

        # Save up-regulated genes if path provided
        if args.out_up_genes:
            ensure_dir(Path(args.out_up_genes).parent)
            Path(args.out_up_genes).write_text("\n".join(up_genes), encoding="utf-8")
            logging.info(f"Saved up-regulated genes: {args.out_up_genes}")

        # Save down-regulated genes if path provided
        if args.out_down_genes:
            ensure_dir(Path(args.out_down_genes).parent)
            Path(args.out_down_genes).write_text("\n".join(down_genes), encoding="utf-8")
            logging.info(f"Saved down-regulated genes: {args.out_down_genes}")


if __name__ == "__main__":
    _main()