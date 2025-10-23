# file: src/analysis/data_loading.py
# ==================================
# Module: data_loading
# ==================================
# This module provides utilities for loading, standardizing, and converting gene expression data from Excel files to a standardized CSV format. It supports flexible column mapping, multiple files and sheets, and configuration via CLI or YAML.
# Functions
# ---------
# - _standardize_columns(df: pd.DataFrame, column_map: Dict[str, str]) -> pd.DataFrame:
#     Standardizes DataFrame columns to "gene", "log2fc", and "padj" using a provided mapping. Handles missing values and enforces numeric types.
# - load_excels(raw_excels: Sequence[str], sheets: Optional[Sequence[str] | str], column_map: Dict[str, str]) -> pd.DataFrame:
#     Loads and standardizes data from multiple Excel files and sheets, concatenating results and annotating source file/sheet. Logs warnings/errors for missing files, sheets, or columns.
# - _parse_args(argv=None) -> argparse.Namespace:
#     Parses CLI arguments for Excel file paths, sheet selection, column mapping, and output CSV path.
# - _main(argv=None) -> None:
#     Main CLI entry point. Loads configuration, parses arguments, loads and standardizes Excel data, and writes output CSV.
# Usage
# -----
# Run as a script to convert Excel gene expression data to a standardized CSV:
#     python data_loading.py --excels file1.xlsx file2.xlsx --gene-col GENE --log2fc-col log2FC --padj-col padj --out-csv output.csv
# Or provide a configuration YAML via --config.
# Dependencies
# ------------
# - pandas
# - numpy
# - argparse
# - logging
# - utils.FileFunctions.ensure_dir
# - utils.config_utils.get_cfg, pick, resolve_path
# - utils.logging_utils_environ.setup_logging
# ==================================

import argparse
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Sequence

import numpy as np
import pandas as pd

from utils.FileFunctions import ensure_dir
from utils.config_utils import get_cfg, pick, resolve_path
from utils.logging_utils_environ import setup_logging

# --- 로그 설정 ---
# 이 함수는 PIPELINE_LOG_FILE 환경 변수를 확인하여
# 이미 존재하는 로그 파일을 사용하거나, 없으면 새로 만듭니다.
logging, _ = setup_logging()

def _standardize_columns(df: pd.DataFrame, column_map: Dict[str, str]) -> pd.DataFrame:
    """
    Standardizes the columns of a DataFrame according to a provided mapping.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame containing gene expression data.
    column_map : Dict[str, str]
        A dictionary mapping standardized column names ("gene", "log2fc", "padj")
        to their corresponding names in the input DataFrame.

    Returns
    -------
    pd.DataFrame
        A new DataFrame with standardized columns: "gene" (as string),
        "log2fc" (as numeric), and "padj" (as numeric, missing values filled with 1.0
        and clipped to a minimum positive value).

    Raises
    ------
    KeyError
        If any required columns specified in `column_map` are missing from the input DataFrame.
    """
    df = df.copy()
    
    missing = [raw for raw in column_map.values() if raw not in df.columns]
    if missing:
        raise KeyError(f"The following required columns are missing from the Excel sheet: {missing}")
        
    std_df = pd.DataFrame({
        "gene": df[column_map["gene"]].astype(str),
        "log2fc": pd.to_numeric(df[column_map["log2fc"]], errors="coerce"),
        "padj": pd.to_numeric(df[column_map["padj"]], errors="coerce"),
    })
    eps = np.nextafter(0, 1)
    std_df["padj"] = std_df["padj"].fillna(1.0).clip(lower=eps)

    other_original_cols = [col for col in df.columns if col not in column_map.values()]
    
    final_df = pd.concat([std_df, df[other_original_cols]], axis=1)
    
    return final_df


def load_excels(raw_excels: Sequence[str], sheets: Optional[Sequence[str] | str], column_map: Dict[str, str]) -> pd.DataFrame:
    """
    Loads and standardizes data from multiple Excel files and sheets.
    Args:
        raw_excels (Sequence[str]): List of file paths to Excel files.
        sheets (Optional[Sequence[str] | str]): List of sheet names to load from each file, 
            or "all" to load all sheets, or None to load the first sheet from each file.
        column_map (Dict[str, str]): Mapping from raw column names to standardized column names.
    Returns:
        pd.DataFrame: Concatenated DataFrame containing standardized data from all specified files and sheets.
            Adds 'source_file' and 'source_sheet' columns to indicate origin of each row.
    Raises:
        RuntimeError: If no data is loaded due to missing files, sheets, or columns.
    Logs:
        Warnings for missing files or sheets.
        Errors for failed column standardization.
        Info on total rows loaded and number of files processed.
    """
    frames: List[pd.DataFrame] = []
    for fpath in raw_excels:
        if not os.path.exists(fpath):
            logging.warning("Excel not found: %s", fpath)
            continue
        xls = pd.ExcelFile(fpath)
        sheet_names_to_load = []
        if sheets is None:
            sheet_names_to_load = [xls.sheet_names[0]] if xls.sheet_names else []
        elif isinstance(sheets, str) and sheets.lower() == "all":
            sheet_names_to_load = xls.sheet_names
        else:
            sheets_list = sheets if isinstance(sheets, list) else [sheets]
            sheet_names_to_load = [s for s in sheets_list if s in xls.sheet_names]
            for s in (set(sheets_list) - set(xls.sheet_names)):
                logging.warning("Sheet not found in %s: %s", fpath, s)
        
        for sheet in sheet_names_to_load:
            raw = pd.read_excel(fpath, sheet_name=sheet, engine=None)
            try:
                std = _standardize_columns(raw, column_map)
                std["source_file"] = os.path.basename(fpath)
                std["source_sheet"] = str(sheet)
                frames.append(std)
            except Exception as e:
                logging.error("Standardization failed: %s | %s | %s", fpath, sheet, e)
                continue
                
    if not frames:
        raise RuntimeError("No data loaded. Check paths/sheets/columns.")
        
    df = pd.concat(frames, ignore_index=True)
    logging.info("Loaded rows=%d from files=%d", len(df), len(raw_excels))
    return df

def create_gsea_expression_matrix(df: pd.DataFrame, gene_col: str, sample_cols: list, output_path: str):
    """Saves the expression data in a GSEA-compatible format (.txt)."""
    if not all(col in df.columns for col in sample_cols):
        logging.error(f"Cannot create GSEA matrix. Not all sample columns defined in YAML were found in the data. Missing: {set(sample_cols) - set(df.columns)}")
        return
        
    gsea_df = pd.DataFrame({"NAME": df[gene_col], "DESCRIPTION": df[gene_col]})
    gsea_df = pd.concat([gsea_df, df[sample_cols]], axis=1)
    
    ensure_dir(Path(output_path).parent)
    gsea_df.to_csv(output_path, sep="\t", index=False, na_rep='NA')
    logging.info(f"Successfully saved GSEA expression matrix to: {output_path}")

def create_gsea_class_labels(class_map: dict, output_path: str):
    """Creates a GSEA-compatible class labels file (.cls)."""
    classes = sorted(class_map.keys())
    num_samples = sum(len(samples) for samples in class_map.values())
    num_classes = len(classes)
    
    line1 = f"{num_samples} {num_classes} 1"
    line2 = f"# {' '.join(classes)}"
    class_labels = [cls for cls in classes for _ in class_map[cls]]

    ensure_dir(Path(output_path).parent)
    with open(output_path, "w") as f:
        f.write(line1 + "\n")
        f.write(line2 + "\n")
        f.write(" ".join(class_labels) + "\n")
    logging.info(f"Successfully saved GSEA class labels to: {output_path}")

def _parse_args(argv=None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Load and standardize data from Excel, with optional GSEA format export.")
    p.add_argument("--config", default=None, help="Path to the main YAML configuration file.")
    p.add_argument("--config-section", default="data_loading", help="Section in the YAML file to use.")
    p.add_argument("--excels", nargs="+", default=None)
    p.add_argument("--sheets", default=None, help='Comma-separated list or "all"')
    p.add_argument("--gene-col", default=None)
    p.add_argument("--log2fc-col", default=None)
    p.add_argument("--padj-col", default=None)
    p.add_argument("--out-csv", default=None)
    return p.parse_args(argv)

def _main(argv=None) -> None:
    args = _parse_args(argv)
    cfg_all = get_cfg(args.config) or {}
    cfg_section = cfg_all.get(args.config_section, {})

    # --- 1. 데이터 로딩 및 표준화 ---
    excel_paths = resolve_path(cli_path=args.excels, cfg=cfg_all, config_key="excel_path", config_section=args.config_section, is_input=True)
    
    # Corrected 'pick' calls
    sheets_arg = pick(args.sheets, cfg_section, "sheets")
    sheets = None if sheets_arg is None else (sheets_arg if sheets_arg == "all" else [s.strip() for s in str(sheets_arg).split(',')])
    
    colmap = {
        "gene": pick(args.gene_col, cfg_section, "gene_col"),
        "log2fc": pick(args.log2fc_col, cfg_section, "log2fc_col"),
        "padj": pick(args.padj_col, cfg_section, "padj_col"),
    }
    
    out_csv_paths = resolve_path(cli_path=[args.out_csv] if args.out_csv else None, cfg=cfg_all, config_key="csv_file", config_section=args.config_section)

    if not excel_paths or not out_csv_paths or any(v is None for v in colmap.values()):
        raise SystemExit("Error: Could not resolve required paths or column names from config or CLI args.")

    out_csv = Path(out_csv_paths[0])
    df = load_excels(excel_paths, sheets, colmap)
    ensure_dir(out_csv.parent)
    df.to_csv(out_csv, index=False)
    logging.info(f"Saved standardized data to: {out_csv}")

    # --- 2. GSEA 파일 생성 ---
    gsea_cfg = cfg_section.get("gsea_outputs")
    if gsea_cfg and gsea_cfg.get("enabled"):
        logging.info("GSEA output generation is enabled.")

        required_keys = ["sample_columns", "expression_matrix_file", "class_labels_file"]
        if any(key not in gsea_cfg for key in required_keys):
            raise SystemExit(f"Error: 'gsea_outputs' is enabled but is missing required keys: {required_keys}")

        output_dir = out_csv.parent
        matrix_file_path = output_dir / gsea_cfg["expression_matrix_file"]
        labels_file_path = output_dir / gsea_cfg["class_labels_file"]

        sample_map = gsea_cfg["sample_columns"]
        all_sample_cols = [col for cols in sample_map.values() for col in cols]
        
        create_gsea_expression_matrix(df, "gene", all_sample_cols, str(matrix_file_path))
        create_gsea_class_labels(sample_map, str(labels_file_path))

if __name__ == "__main__":
    _main()