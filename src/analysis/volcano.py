# ===============================
# file: src/analysis/volcano.py
# ===============================
# This module provides functions and a command-line interface for generating volcano plots from standardized gene expression data.
# It allows for customization of statistical thresholds, plot limits, and gene annotation.
#
# Functions
# ---------
# - plot_volcano(df: pd.DataFrame, out_path: str, padj_cutoff: float, log2fc_cutoff: float, ...) -> plt.Axes:
#     Creates and saves a volcano plot from a DataFrame, highlighting significant genes and optionally annotating specific ones.
# - _parse_args(argv=None) -> argparse.Namespace:
#     Parses command-line arguments for input/output files, plot parameters, and configuration.
# - _main(argv=None) -> None:
#     The main entry point for the command-line script. It loads data and configuration, then generates the volcano plot.
#
# Usage
# -----
# Run as a script to generate a volcano plot from a standardized CSV file:
#     python volcano.py --in-csv standardized.csv --out-png volcano.png --padj-cutoff 0.05 --log2fc-cutoff 1.0
#
# Dependencies
# ------------
# - pandas
# - numpy
# - matplotlib
# - argparse
# - utils.FileFunctions, utils.OmicsFunctions, utils.config_utils

import argparse
import os
from pathlib import Path
from typing import Dict, Iterable, Optional, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from utils.FileFunctions import ensure_dir 
from utils.OmicsFunctions import read_gene_list
from utils.config_utils import get_cfg, pick, resolve_path
from utils.logging_utils_environ import setup_logging

# This function intelligently finds the log file set by the notebook.
logging, _ = setup_logging()

def plot_volcano(
    df: pd.DataFrame,
    out_path: str,
    padj_cutoff: float,
    log2fc_cutoff: float,
    xlim: Optional[Tuple[Optional[float], Optional[float]]] = None,
    ylim: Optional[Tuple[Optional[float], Optional[float]]] = None,
    annotate_genes: Optional[Iterable[str]] = None,
    max_labels: int = 30,
    colors: Optional[Dict[str, str]] = None,
) -> plt.Axes:
    """
    Create and save a volcano plot; returns the Axes for inspection.

    Config keys (YAML section: `volcano`)
    - in_csv, out_png, padj_cutoff, log2fc_cutoff, xlim, ylim, annotate, max_labels

    Note: The returned Axes belongs to a figure that is saved then closed.
    Use the return value only for quick inspection/testing.
    """
    colors = colors or {"up": "#d62728", "down": "#1f77b4", "other": "#7f7f7f"}
    df = df.copy()
    df["neglog10_padj"] = -np.log10(df["padj"].clip(lower=np.nextafter(0, 1)))

    up = (df["padj"] < padj_cutoff) & (df["log2fc"] >= log2fc_cutoff)
    down = (df["padj"] < padj_cutoff) & (df["log2fc"] <= -abs(log2fc_cutoff))

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(df.loc[~(up | down), "log2fc"], df.loc[~(up | down), "neglog10_padj"], s=12, alpha=0.6, c=colors["other"], label="Other")
    ax.scatter(df.loc[up, "log2fc"], df.loc[up, "neglog10_padj"], s=16, alpha=0.9, c=colors["up"], label="Up")
    ax.scatter(df.loc[down, "log2fc"], df.loc[down, "neglog10_padj"], s=16, alpha=0.9, c=colors["down"], label="Down")

    ax.axhline(-np.log10(padj_cutoff), linestyle="--", linewidth=1)
    if log2fc_cutoff != 0:
        ax.axvline(log2fc_cutoff, linestyle="--", linewidth=1)
        ax.axvline(-log2fc_cutoff, linestyle="--", linewidth=1)

    if annotate_genes:
        gset = set(df["gene"])
        for g in list(annotate_genes)[:max_labels]:
            if g not in gset:
                continue
            row = df[df["gene"] == g].head(1)
            x = float(row["log2fc"].iloc[0]); y = float(row["neglog10_padj"].iloc[0])
            ax.annotate(g, (x, y), xytext=(3, 3), textcoords="offset points", fontsize=8,
                        arrowprops=dict(arrowstyle="-", lw=0.3, alpha=0.6))

    ax.set_xlabel("log2FC"); ax.set_ylabel("-log10(padj)"); ax.legend(frameon=False); ax.grid(alpha=0.2)
    if xlim: ax.set_xlim(*xlim)
    if ylim: ax.set_ylim(*ylim)

    ensure_dir(Path(out_path).parent.as_posix())
    fig.tight_layout(); fig.savefig(out_path, dpi=300); plt.close(fig)
    return ax


# -------- CLI: standardized CSV -> volcano.png --------

def _parse_args(argv=None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Volcano plot from standardized CSV")
    p.add_argument("--config", default=None, help="pipeline.yaml or volcano.yaml")
    p.add_argument("--config-section", default="volcano", help="YAML section name")
    p.add_argument("--in-csv", default=None)
    p.add_argument("--out-png", default=None)
    p.add_argument("--padj-cutoff", type=float, default=None)
    p.add_argument("--log2fc-cutoff", type=float, default=None)
    p.add_argument("--xlim", default=None, help="-8,8")
    p.add_argument("--ylim", default=None, help="0,20")
    p.add_argument("--annotate", default=None, help="Gene list file")
    p.add_argument("--max-labels", type=int, default=None)
    return p.parse_args(argv)


def _to_tuple_2(s: Optional[str]):
    if not s: return None
    parts = [x.strip() for x in s.split(',') if x.strip()]
    return (float(parts[0]), float(parts[1])) if len(parts) == 2 else None


def _main(argv=None) -> None:
    args = _parse_args(argv)
    cfg_all = get_cfg(args.config) or {}
    # Allow single-file YAML with sections.
    cfg_section = cfg_all.get(args.config_section, cfg_all)

    # Resolve input CSV path
    in_csv_paths = resolve_path(
        cli_path=[args.in_csv] if args.in_csv else None,
        cfg=cfg_all,
        config_key="in_csv_file",
        config_section=args.config_section,
    )
    in_csv = in_csv_paths[0]

    # Resolve output png path
    out_png_paths = resolve_path(
        cli_path=[args.out_png] if args.out_png else None,
        cfg=cfg_all,
        config_key="out_png_file",
        config_section=args.config_section,
    )
    out_png = out_png_paths[0]

    padj = pick(args.padj_cutoff, cfg_section, "padj_cutoff", 0.05)
    l2fc = pick(args.log2fc_cutoff, cfg_section, "log2fc_cutoff", 1.0)
    xlim = _to_tuple_2(args.xlim) if args.xlim else cfg_section.get("xlim")
    ylim = _to_tuple_2(args.ylim) if args.ylim else cfg_section.get("ylim")
    max_labels = pick(args.max_labels, cfg_section, "max_labels", 30)

    # Resolve optional annotation file path
    annotate_paths = resolve_path(
        cli_path=[args.annotate] if args.annotate else None, 
        cfg=cfg_all, config_key="annotate_file", config_section=args.config_section,
        is_input=True  # Treat as an input file, relative to project root
    )
    annotate_file = annotate_paths[0] if annotate_paths else None
    
    if not in_csv or not out_png:
        raise SystemExit("Provide --config or both --in-csv and --out-png")

    df = pd.read_csv(in_csv)
    genes = read_gene_list(annotate_file) if annotate_file else None
    plot_volcano(df, out_png, padj, l2fc, xlim=xlim, ylim=ylim,
                annotate_genes=genes, max_labels=int(max_labels))
    logging.info(f"Saved: {out_png}")


if __name__ == "__main__":
    _main()