# ================================
# file: src/analysis/go_enrich.py
# ================================
# This module performs Gene Ontology (GO) enrichment analysis on gene lists using the GOATOOLS library.
# It identifies over-represented GO terms in a given set of study genes compared to a background gene population.
# The script can be configured via command-line arguments or a YAML file.
#
# Functions
# ---------
# - run_go_enrichment(genes: Sequence[str], background: Sequence[str], obo_path: str, gaf_path: str, ...) -> Optional[pd.DataFrame]:
#     Performs GO enrichment analysis for a given list of genes against a background set.
# - _parse_args(argv=None) -> argparse.Namespace:
#     Parses command-line arguments for input files (gene lists, background), GO resources (OBO, GAF), and analysis parameters.
# - _main(argv=None) -> None:
#     The main entry point for the command-line script. It loads configuration and data, then runs the enrichment analysis for one or more gene sets (e.g., up/down-regulated).
#
# Usage
# -----
# Run as a script to perform GO enrichment analysis from a filtered gene list:
#     python go_enrich.py --config configs/GO_pipeline.yaml
#
# Dependencies
# ------------
# - pandas
# - goatools (optional, but required for core functionality)
# - argparse
# - utils.FileFunctions, utils.OmicsFunctions, utils.config_utils
import argparse
import io
import sys
from contextlib import redirect_stdout, redirect_stderr
import logging
from pathlib import Path
from typing import Optional, Sequence
import pandas as pd

from utils.FileFunctions import ensure_dir 
from utils.OmicsFunctions import read_gene_list, load_symbol_assoc_from_gaf
from utils.config_utils import get_cfg, pick, resolve_path
from utils.logging_utils_environ import setup_logging

# This function intelligently finds the log file set by the notebook.
log, _ = setup_logging()

# Import goatools directly as a required dependency
from goatools.obo_parser import GODag
from goatools.associations import read_gaf
from goatools.goea.go_enrichment_ns import GOEnrichmentStudy

# --- _GO 변수 정의 추가 ---
# goatools는 선택적 의존성으로 유지합니다.
try:
    from goatools.obo_parser import GODag
    from goatools.associations import read_gaf
    from goatools.goea.go_enrichment_ns import GOEnrichmentStudy
    _GO = True
except ImportError:
    _GO = False

def run_go_enrichment(
    genes: Sequence[str],
    background: Sequence[str],
    obo_path: Optional[str],
    gaf_path: Optional[str],
    alpha: float = 0.05,
    multiple_testing: str = "fdr_bh",
    taxon: str = "9606",
    aspect: str = "all",
) -> Optional[pd.DataFrame]:
    """Run GOATOOLS enrichment; returns a sorted DataFrame or None."""
    # --- 모든 로그 캡처 시도를 제거하고 원래 로직으로 복귀 ---
    if not _GO:
        log.warning("GOATOOLS not available; skipping GOEA.")
        return None
    if not (obo_path and Path(obo_path).exists() and gaf_path and Path(gaf_path).exists()):
        log.warning("GO resources missing; skipping GOEA.")
        return None

    go_dag = GODag(obo_path, optional_attrs={'relationship'})
    assoc = load_symbol_assoc_from_gaf(gaf_path, taxon=taxon, aspect=aspect)

    genes_set = [g for g in genes if g in assoc]
    if not genes_set:
        log.warning("No overlap between study genes and GAF; skipping GOEA.")
        return None

    pop = [g for g in background if g in assoc] or list(assoc.keys())

    study = GOEnrichmentStudy(pop, assoc, go_dag, alpha=alpha, methods=[multiple_testing])
    
    # 이제 goatools는 화면에 자유롭게 출력하도록 내버려 둡니다.
    results = study.run_study(genes_set)

    rows = []
    for r in results:
        padj = getattr(r, f"p_{multiple_testing}", getattr(r, "p_fdr_bh", None))
        if padj is None:
            padj = r.p_uncorrected
        rows.append({
            "GO_ID": r.GO,
            "NS": r.NS,
            "Term": r.name,
            "study_count": r.study_count,
            "study_n": r.study_n,
            "pop_count": r.pop_count,
            "pop_n": r.pop_n,
            "p_uncorr": r.p_uncorrected,
            "p_adj": padj,
            "depth": r.depth,
        })
    df = pd.DataFrame(rows)
    if df.empty:
        log.warning("GOEA returned empty results.")
        return None
    df.sort_values(["NS", "p_adj", "study_count"], ascending=[True, True, False], inplace=True)
    return df


# -------- CLI: genes/background -> goea_results.csv --------

def _parse_args(argv=None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="GO enrichment with GOATOOLS")
    p.add_argument("--config", default=None, help="pipeline.yaml or go_enrich.yaml")
    p.add_argument("--config-section", default="go_enrich", help="YAML section name")
    src = p.add_mutually_exclusive_group()
    src.add_argument("--genes-file", help="Single gene list file for analysis.")
    src.add_argument("--filtered-csv", help="Filtered CSV to extract all genes.")
    src.add_argument("--up-genes-file", help="Gene list for up-regulated set.")
    src.add_argument("--down-genes-file", help="Gene list for down-regulated set.")

    p.add_argument("--background-csv", default=None)
    p.add_argument("--obo", default=None)
    p.add_argument("--gaf", default=None)
    p.add_argument("--alpha", type=float, default=None)
    p.add_argument("--mt", default=None)
    p.add_argument("--taxon", default=None) # Add this line
    p.add_argument("--out-up-csv", default=None)
    p.add_argument("--out-down-csv", default=None)
    p.add_argument("--out-csv", default=None)
    return p.parse_args(argv)


def _main(argv=None) -> None:
    args = _parse_args(argv)
    cfg_all = get_cfg(args.config) or {}
    cfg_section = cfg_all.get(args.config_section, cfg_all)
    
    # --- Analysis parameters from config ---
    alpha = pick(args.alpha, cfg_section, "alpha", 0.05)
    mt = pick(args.mt, cfg_section, "mt", "fdr_bh")
    taxon = pick(args.taxon, cfg_section, "taxon", "9606")

    # --- Reference files (project-root-relative) ---
    obo_paths = resolve_path(
        cli_path=[args.obo] if args.obo else None,
        cfg=cfg_all, config_key="obo", config_section=args.config_section,
        is_input=True
    )
    obo = obo_paths[0] if obo_paths else None

    gaf_paths = resolve_path(
        cli_path=[args.gaf] if args.gaf else None,
        cfg=cfg_all, config_key="gaf", config_section=args.config_section,
        is_input=True
    )
    gaf = gaf_paths[0] if gaf_paths else None

    if not obo or not gaf:
        raise SystemExit("Error: GO reference files (obo, gaf) are required")

    # --- Background genes (from CLI or inferred) ---
    background_csv = args.background_csv if args.background_csv else None
    if background_csv and Path(background_csv).exists():
        bg = pd.read_csv(background_csv)["gene"].dropna().astype(str).unique().tolist()
    else:
        bg = []
        log.warning("No background CSV provided. Using study genes as background, which may bias results.")

    # --- Process each gene set (all, up, down) ---
    # Map output files to their corresponding input gene files
    tasks = []
    
    if args.filtered_csv and args.out_csv:
        tasks.append(("all", args.filtered_csv, args.out_csv, "filtered_csv"))
    if args.up_genes_file and args.out_up_csv:
        tasks.append(("up", args.up_genes_file, args.out_up_csv, "genes_file"))
    if args.down_genes_file and args.out_down_csv:
        tasks.append(("down", args.down_genes_file, args.out_down_csv, "genes_file"))

    for label, in_path, out_path, file_type in tasks:
        if file_type == "filtered_csv":
            genes = pd.read_csv(in_path)["gene"].dropna().astype(str).unique().tolist()
        else:  # genes_file
            genes = sorted(read_gene_list(in_path))

        if not genes:
            log.warning(f"Skipping {label}: No genes found in {in_path}")
            continue

        df_go = run_go_enrichment(genes, bg or genes, obo, gaf, alpha=alpha, multiple_testing=mt, taxon=taxon)
        if df_go is None:
            log.info(f"GOEA for {label} skipped or empty; nothing saved to {out_path}.")
            continue
        
        ensure_dir(Path(out_path).parent.as_posix())
        df_go.to_csv(out_path, index=False)
        log.info(f"Successfully saved GO enrichment results ({label}) to {out_path}")


if __name__ == "__main__":
    _main()