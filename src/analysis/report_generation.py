# ==============================================
# file: src/analysis/report_generation.py (new)
# ==============================================
"""
Lightweight HTML report generator for the GO pipeline.

Inputs (YAML section: `report`)
- standardized_csv: standardized DE table
- filtered_csv: filtered DE genes table
- volcano_png: path to volcano plot
- goea_csv: GO enrichment results (CSV)
- go_barplot_png: path to GO barplot
- out_html: output HTML path
- title, sample_name, author (optional meta)

Why HTML? Works everywhere, easy to email or archive.
"""
import argparse
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd

from utils.FileFunctions import ensure_dir
from utils.config_utils import get_cfg, pick, resolve_path
from utils.logging_utils_environ import setup_logging

# This function intelligently finds the log file set by the notebook.
log, _ = setup_logging()


def _summarize_counts(std_csv: str, filt_csv: str) -> dict:
    std = pd.read_csv(std_csv)
    filt = pd.read_csv(filt_csv)
    n_total = len(std)
    n_sig = len(filt)
    n_up = int((filt["log2fc"] > 0).sum())
    n_down = int((filt["log2fc"] < 0).sum())
    return {
        "n_total": int(n_total),
        "n_sig": int(n_sig),
        "n_up": n_up,
        "n_down": n_down,
    }


def _top_go(go_csv: Optional[str], k: int = 20) -> pd.DataFrame:
    if not go_csv or not Path(go_csv).exists():
        return pd.DataFrame(columns=["NS", "GO_ID", "Term", "p_adj", "study_count"])
    df = pd.read_csv(go_csv)
    if "p_adj" not in df.columns and "p.adjust" in df.columns:
        df = df.rename(columns={"p.adjust": "p_adj"})
    cols = [c for c in ["NS", "GO_ID", "Term", "p_adj", "study_count"] if c in df.columns]
    order = df.sort_values(["NS", "p_adj", "study_count"], ascending=[True, True, False])
    return order[cols].groupby("NS", as_index=False, group_keys=False).head(k)


def build_report_html(std_csv: str, filt_csv: str, volcano_png: str,
                      go_csv: Optional[str], go_bar_png: str,
                      go_up_csv: Optional[str], go_up_bar_png: Optional[str],
                      go_down_csv: Optional[str], go_down_bar_png: Optional[str],
                      title: str, sample_name: str, author: Optional[str] = None) -> str:
    meta = _summarize_counts(std_csv, filt_csv)
    go_top = _top_go(go_csv, 20)
    go_up_top = _top_go(go_up_csv, 15)
    go_down_top = _top_go(go_down_csv, 15)

    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    author = author or ""

    volcano_png = "./" + Path(volcano_png).name
    go_bar_png = "./" + Path(go_bar_png).name
    go_up_bar_png_rel = ("./" + Path(go_up_bar_png).name) if go_up_bar_png and Path(go_up_bar_png).exists() else ""
    go_down_bar_png_rel = ("./" + Path(go_down_bar_png).name) if go_down_bar_png and Path(go_down_bar_png).exists() else ""

    go_up_table_html = (
        "<p>No GO enrichment results for up-regulated genes.</p>" if go_up_top.empty else go_up_top.to_html(index=False, escape=False)
    )
    go_down_table_html = (
        "<p>No GO enrichment results for down-regulated genes.</p>" if go_down_top.empty else go_down_top.to_html(index=False, escape=False)
    )

    go_table_html = (
        "<p>No GO enrichment results available.</p>" if go_top.empty else
        go_top.to_html(index=False, escape=False)
    )

    html = f"""
<!DOCTYPE html>
<html lang="en">\n<head>\n<meta charset="utf-8">\n<title>{title}</title>\n<style>
body{{font-family:ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial;max-width:980px;margin:2rem auto;padding:0 1rem;color:#222}}
h1,h2{{margin:0.2rem 0 0.6rem}}
.card{{border:1px solid #e5e7eb;border-radius:12px;padding:16px;margin:12px 0;box-shadow:0 1px 2px rgba(0,0,0,.04)}}
.kv{{display:grid;grid-template-columns:160px 1fr;gap:8px}}
img{{max-width:100%;height:auto;border-radius:8px;border:1px solid #e5e7eb}}
table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #e5e7eb;padding:6px 8px;text-align:left}}th{{background:#f9fafb}}
.footer{{color:#6b7280;font-size:12px;margin-top:24px}}
</style>\n</head>\n<body>
<h1>{title}</h1>
<div class="kv card">\n<div><strong>Sample</strong></div><div>{sample_name}</div>
<div><strong>Generated</strong></div><div>{today}</div>
<div><strong>Author</strong></div><div>{author}</div>
<div><strong>Totals</strong></div><div>All: {meta['n_total']}, Filtered: {meta['n_sig']} (Up {meta['n_up']}, Down {meta['n_down']})</div>
</div>

<h2>Volcano Plot</h2>
<div class="card"><img src="{volcano_png}" alt="volcano plot"></div>

<h2>Top GO Terms</h2>
<div class="card">{go_table_html}</div>

<h2>GO Bar Plot</h2>
<div class="card"><img src="{go_bar_png}" alt="go barplot"></div>

<h2>Top GO Terms (Up-regulated)</h2>
<div class="card">{go_up_table_html}</div>
<h2>GO Bar Plot (Up-regulated)</h2>
<div class="card">{f'<img src="{go_up_bar_png_rel}" alt="go up barplot">' if go_up_bar_png_rel else "<p>Plot not available.</p>"}</div>


<h2>Top GO Terms (Down-regulated)</h2>
<div class="card">{go_down_table_html}</div>
<h2>GO Bar Plot (Down-regulated)</h2>
<div class="card">{f'<img src="{go_down_bar_png_rel}" alt="go down barplot">' if go_down_bar_png_rel else "<p>Plot not available.</p>"}</div>


<div class="footer">Generated by report_generation.py</div>
</body></html>
"""
    return html


def _parse_args(argv=None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate HTML report for the GO pipeline")
    p.add_argument("--config", default=None, help="pipeline.yaml or report.yaml")
    p.add_argument("--config-section", default="report", help="YAML section name")
    p.add_argument("--standardized-csv", default=None)
    p.add_argument("--filtered-csv", default=None)
    p.add_argument("--volcano-png", default=None)
    p.add_argument("--goea-csv", default=None)
    p.add_argument("--go-barplot-png", default=None)
    p.add_argument("--goea-up-csv", default=None)
    p.add_argument("--go-up-barplot-png", default=None)
    p.add_argument("--goea-down-csv", default=None)
    p.add_argument("--go-down-barplot-png", default=None)
    p.add_argument("--out-html", default=None)
    p.add_argument("--title", default=None)
    p.add_argument("--sample-name", default=None)
    p.add_argument("--author", default=None)
    return p.parse_args(argv)


def _main(argv=None) -> None:
    args = _parse_args(argv)
    cfg_all = get_cfg(args.config) or {}
    cfg_section = cfg_all.get(args.config_section, {})

    # --- Resolve all paths consistently ---
    # Helper to resolve a single optional path.
    # These are all intermediate files, so they are relative to ROOT_DIR (is_input=False).
    def _resolve_single_path(arg_val, key):
        paths = resolve_path(
            cli_path=[arg_val] if arg_val else None,
            cfg=cfg_all, config_key=key, config_section=args.config_section
        )
        # Return path only if it exists, as these are optional inputs
        path = paths[0] if paths else None
        return path if (path and Path(path).exists()) else None

    # Resolve all required and optional paths
    std_csv = _resolve_single_path(args.standardized_csv, "standardized_csv_file")
    filt_csv = _resolve_single_path(args.filtered_csv, "filtered_csv_file")
    volcano_png = _resolve_single_path(args.volcano_png, "volcano_png_file")
    go_bar_png = _resolve_single_path(args.go_barplot_png, "go_barplot_png_file")
    
    # The main GOEA result is optional
    go_csv = _resolve_single_path(args.goea_csv, "goea_csv_file")

    # Up/Down regulated results are also optional
    go_up_csv = _resolve_single_path(args.goea_up_csv, "goea_up_csv_file")
    go_up_png = _resolve_single_path(args.go_up_barplot_png, "go_up_barplot_png_file")
    go_down_csv = _resolve_single_path(args.goea_down_csv, "goea_down_csv_file")
    go_down_png = _resolve_single_path(args.go_down_barplot_png, "go_down_barplot_png_file")
    
    # Output path is required
    out_html_paths = resolve_path(cli_path=[args.out_html] if args.out_html else None, cfg=cfg_all, config_key="out_html_file", config_section=args.config_section)
    out_html = out_html_paths[0] if out_html_paths else None

    # Pick non-path parameters
    title = pick(args.title, cfg_section, "title", "GO Analysis Report")
    sample_name = pick(args.sample_name, cfg_section, "sample_name", "")
    author = pick(args.author, cfg_section, "author", "")

    if not (std_csv and filt_csv and volcano_png and go_bar_png and out_html):
        raise SystemExit("Missing required inputs: std_csv, filt_csv, volcano_png, go_barplot_png, out_html")

    html = build_report_html(
        std_csv, filt_csv, volcano_png,
        go_csv, go_bar_png, go_up_csv, go_up_png, go_down_csv, go_down_png,
        title, sample_name, author
    )
    ensure_dir(Path(out_html).parent.as_posix())
    Path(out_html).write_text(html, encoding="utf-8")
    log.info(f"Saved: {out_html}")


if __name__ == "__main__":
    _main()