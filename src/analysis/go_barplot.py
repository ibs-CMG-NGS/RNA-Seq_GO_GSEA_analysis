# =================================
# file: src/analysis/go_barplot.py
# =================================
import argparse
import logging

# =================================
# This module provides functions and a command-line interface for generating bar plots from Gene Ontology (GO) enrichment analysis results.
# It visualizes the top N most significant GO terms for specified namespaces (e.g., BP, MF, CC).
#
# Functions
# ---------
# - plot_go_bar(go_df: pd.DataFrame, out_path: str, top_n: int, namespaces: Sequence[str]) -> plt.Axes:
#     Creates and saves a horizontal bar plot of top GO terms from a DataFrame.
# - _parse_args(argv=None) -> argparse.Namespace:
#     Parses command-line arguments for input/output files, plot parameters, and configuration.
# - _main(argv=None) -> None:
#     The main entry point for the command-line script. It loads data and configuration, then generates one or more bar plots.
#
# Usage
# -----
# Run as a script to generate a bar plot from a GOEA results CSV file:
#     python go_barplot.py --in-csv goea_results.csv --out-png go_barplot.png --top-n 15 --namespaces BP,MF
#
# Dependencies
# ------------
# - pandas, numpy, matplotlib, argparse
# - utils.FileFunctions, utils.config_utils

from pathlib import Path
from typing import Sequence

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from utils.FileFunctions import ensure_dir 
from utils.OmicsFunctions import read_gene_list
from utils.config_utils import get_cfg, pick, resolve_path
from utils.logging_utils_environ import setup_logging

# This function intelligently finds the log file set by the notebook.
log, _ = setup_logging()

def plot_go_bar(go_df: pd.DataFrame, out_path: str, top_n: int = 12,
                namespaces: Sequence[str] = ("BP", "MF", "CC")) -> plt.Axes:
    """
    Create a horizontal bar plot of top GO terms per namespace and save.

    Config keys (YAML section: `go_barplot`)
    - in_csv, out_png, top_n, namespaces
    """
    df = go_df.copy()
    if "p_adj" not in df.columns:
        if "p.adjust" in df.columns:
            df = df.rename(columns={"p.adjust": "p_adj"})
        else:
            raise KeyError("GO DF must contain 'p_adj' or 'p.adjust'")
    if namespaces and len(namespaces) == 1 and namespaces[0] == "ALL":
        namespaces = sorted(df["NS"].dropna().unique().tolist())

    groups = []
    for ns in namespaces:
        sub = df[df["NS"] == ns].nsmallest(top_n, "p_adj").copy()
        sub["label"] = sub["Term"].astype(str)
        sub["neglog10_padj"] = -np.log10(sub["p_adj"].clip(lower=np.nextafter(0, 1)))
        sub["Namespace"] = ns
        groups.append(sub)

    top_df = pd.concat(groups, ignore_index=True) if groups else df.head(0)

    unique_ns = list(dict.fromkeys(top_df["Namespace"].tolist()))
    nrows = max(1, len(unique_ns))
    colors = {"BP": "#1f77b4", "MF": "#ff7f0e", "CC": "#2ca02c", "default": "#7f7f7f"}
    fig, axes = plt.subplots(nrows=nrows, ncols=1, figsize=(10, 3*nrows), squeeze=False)
    for ax, ns in zip(axes[:, 0], unique_ns):
        dd = top_df[top_df["Namespace"] == ns].sort_values("neglog10_padj")
        color = colors.get(ns, colors["default"])
        ax.barh(dd["label"], dd["neglog10_padj"], color=color)
        ax.set_title(f"GO {ns} (Top {top_n})")
        ax.set_xlabel("-log10(padj)")
        ax.grid(axis="x", alpha=0.2)
    ensure_dir(Path(out_path).parent.as_posix())
    fig.tight_layout(); fig.savefig(out_path, dpi=300); plt.close(fig)
    return axes[-1, 0]


# -------- CLI: goea_results.csv -> go_barplot.png --------

def _parse_args(argv=None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="GO bar plot from GOEA CSV")
    p.add_argument("--config", default=None, help="pipeline.yaml or go_barplot.yaml")
    p.add_argument("--config-section", default="go_barplot", help="YAML section name")
    p.add_argument("--in-csv", default=None, help="Input for combined plot")
    p.add_argument("--out-png", default=None, help="Output for combined plot")
    p.add_argument("--in-up-csv", default=None, help="Input for up-regulated plot")
    p.add_argument("--out-up-png", default=None, help="Output for up-regulated plot")
    p.add_argument("--in-down-csv", default=None, help="Input for down-regulated plot")
    p.add_argument("--out-down-png", default=None, help="Output for down-regulated plot")
    p.add_argument("--top-n", type=int, default=None)
    p.add_argument("--namespaces", default=None, help='Comma list or "ALL"')
    return p.parse_args(argv)


def _main(argv=None) -> None:
    args = _parse_args(argv)
    cfg_all = get_cfg(args.config) or {}
    # Allow single-file YAML with sections.
    cfg_section = cfg_all.get(args.config_section, cfg_all)

    top_n = pick(args.top_n, cfg_section, "top_n", 12)
    ns = pick(args.namespaces, cfg_section, "namespaces", ["BP", "MF", "CC"])
    if isinstance(ns, str) and ns != "ALL":
        ns = [x.strip() for x in ns.split(',') if x.strip()]

    # Define pairs of input CSVs and their corresponding output PNGs
    plot_tasks = {
        "main": (args.in_csv, args.out_png, "goea_csv_file", "out_png_file", "go_enrich"),
        "up": (args.in_up_csv, args.out_up_png, "goea_up_csv_file", "out_up_png_file", "go_enrich"),
        "down": (args.in_down_csv, args.out_down_png, "goea_down_csv_file", "out_down_png_file", "go_enrich"),
    }

    for task_name, (cli_in, cli_out, cfg_in_key, cfg_out_key, in_section) in plot_tasks.items():
        # Resolve paths for input and output. These are intermediate files,
        # so they should be relative to the sample's ROOT_DIR (is_input=False).
        in_paths = resolve_path(
            cli_path=[cli_in] if cli_in else None,
            cfg=cfg_all, config_key=cfg_in_key, config_section=in_section
        )
        out_paths = resolve_path(
            cli_path=[cli_out] if cli_out else None,
            cfg=cfg_all, config_key=cfg_out_key, config_section=args.config_section # Output is in its own section
        )

        if in_paths and out_paths:
            in_csv = in_paths[0]
            out_png = out_paths[0]
            if not Path(in_csv).exists():
                log.warning(f"Skipping plot for '{task_name}': Input file not found: {in_csv}")
                continue
            df = pd.read_csv(in_csv)
            plot_go_bar(df, out_png, top_n=int(top_n), namespaces=ns if ns else ("BP", "MF", "CC"))
            log.info(f"Saved: {out_png}")


if __name__ == "__main__":
    _main()