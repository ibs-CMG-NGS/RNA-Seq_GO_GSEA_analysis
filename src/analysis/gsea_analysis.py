# =====================================
# file: src/analysis/gsea_analysis.py
"""
gsea_analysis.py
This module provides functions and a command-line interface for performing Gene Set Enrichment Analysis (GSEA) using the `gseapy` library. It supports both Pre-ranked and Classic GSEA modes, allowing users to analyze gene expression data with custom or standard gene sets.
Functions:
----------
- run_gsea_prerank(ranked_gene_list, gene_sets, output_dir):
    Runs GSEA Pre-ranked analysis using a ranked list of genes and specified gene sets.
    Parameters:
        ranked_gene_list (pd.DataFrame): DataFrame with gene symbols and ranking metric.
        gene_sets (str): Name of gene set library or path to GMT file.
        output_dir (Path): Directory to save GSEA results.
    Returns:
        GSEApy prerank results object or None if an error occurs.
- run_gsea_classic(expression_df, class_labels_path, gene_sets, output_dir):
    Runs Classic GSEA analysis using an expression matrix and class labels.
    Parameters:
        expression_df (pd.DataFrame): Gene expression matrix.
        class_labels_path (str): Path to .cls file with class labels.
        gene_sets (str): Name of gene set library or path to GMT file.
        output_dir (Path): Directory to save GSEA results.
    Returns:
        GSEApy gsea results object or None if an error occurs.
- _parse_args(argv=None):
    Parses command-line arguments for configuration file and section.
    Parameters:
        argv (list, optional): List of command-line arguments.
    Returns:
        argparse.Namespace: Parsed arguments.
- _main(argv=None):
    Main function to run GSEA analysis from the command line.
    Reads configuration, determines mode, loads input data, and runs the appropriate GSEA analysis.
    Parameters:
        argv (list, optional): List of command-line arguments.
Usage:
------
This script can be run as a standalone program to perform GSEA analysis based on a YAML configuration file. It supports both Pre-ranked and Classic GSEA workflows.
Example command:
    python gsea_analysis.py --config path/to/config.yaml --config-section gsea
Dependencies:
-------------
- gseapy
- pandas
- argparse
- logging
- pathlib
- utils.FileFunctions
- utils.config_utils
- utils.logging_utils_environ
"""
# =====================================

import argparse
import logging
import re
import traceback
from pathlib import Path

import gseapy as gp
import pandas as pd

# YG_utils_analysis에서 제공하는 유틸리티 함수들
from utils.FileFunctions import ensure_dir
from utils.config_utils import get_cfg, pick, resolve_path
from utils.logging_utils_environ import setup_logging

# --- 로그 설정 ---
# 이 함수는 PIPELINE_LOG_FILE 환경 변수를 확인하여
# 이미 존재하는 로그 파일을 사용하거나, 없으면 새로 만듭니다.
log, _ = setup_logging()

def get_sheet_name(gene_set_path: str) -> str:
    """GMT 파일 경로 또는 라이브러리 이름으로부터 Excel 시트 이름을 생성합니다."""
    name = Path(gene_set_path).stem
    name = re.sub(r'\.v\d+.*', '', name)
    return name[:31]

def write_results_to_excel(results_dict: dict, output_path: str):
    """여러 GSEA 결과 데이터프레임을 하나의 Excel 파일에 시트별로 저장합니다."""
    log.info(f"모든 GSEA 결과를 하나의 Excel 파일로 통합 중: {output_path}")
    try:
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            for sheet_name, df in results_dict.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        log.info("✅ GSEA 리포트(Excel 파일) 생성이 완료되었습니다.")
    except Exception as e:
        log.error(f"Excel 파일 생성 중 오류 발생: {e}")

def run_gsea_prerank(ranked_list: pd.DataFrame, gene_sets: str, outdir: Path, params: dict):
    """GSEA Pre-ranked를 실행하고 결과 데이터프레임을 반환합니다."""
    log.info(f"--- GSEA Pre-ranked 분석 시작: '{Path(gene_sets).name}' ---")
    ensure_dir(str(outdir))
    try:
        results = gp.prerank(
            rnk=ranked_list,
            gene_sets=gene_sets,
            outdir=str(outdir),
            min_size=params.get("min_size", 15),
            max_size=params.get("max_size", 500),
            permutation_num=params.get("permutation_num", 1000),
            weight=params.get("weighting_exponent", 1),
            seed=params.get("seed", 42),
            verbose=True
        )
        return results.res2d
    except Exception as e:
        log.error(f"GSEA Pre-ranked 분석 중 오류 발생: {e}")
        log.debug(traceback.format_exc())
        return None

def run_gsea_classic(expression_df: pd.DataFrame, class_labels_path: str, gene_sets: str, outdir: Path, params: dict):
    """Classic GSEA를 실행하고 결과 데이터프레임을 반환합니다."""
    log.info(f"--- Classic GSEA 분석 시작: '{Path(gene_sets).name}' ---")
    ensure_dir(str(outdir))
    try:
        results = gp.gsea(
            data=expression_df,
            gene_sets=gene_sets,
            cls=class_labels_path,
            outdir=str(outdir),
            min_size=params.get("min_size", 15),
            max_size=params.get("max_size", 500),
            permutation_num=params.get("permutation_num", 1000),
            seed=params.get("seed", 42),
            verbose=True
        )
        return results.res2d
    except Exception as e:
        log.error(f"Classic GSEA 분석 중 오류 발생: {e}")
        log.debug(traceback.format_exc())
        return None

def _parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Perform GSEA screening for multiple gene sets.")
    parser.add_argument("--config", required=True, help="Path to the main YAML configuration file.")
    parser.add_argument("--config-section", default="gsea", help="The section in the YAML file to use.")
    parser.add_argument("--mode", default=None, help="GSEA mode: 'prerank' or 'classic'. Overrides config.")
    return parser.parse_args(argv)

def _main(argv=None):
    args = _parse_args(argv)
    cfg_all = get_cfg(args.config)
    cfg_section = cfg_all.get(args.config_section, {})

    mode = pick(args.mode, cfg_section, "mode", "prerank").lower()
    log.info(f"GSEA 스크리닝 모드: '{mode}'")

    # --- 상세 파라미터를 딕셔너리로 읽어오기 ---
    gsea_params = {
        "min_size": pick(None, cfg_section, "min_size", 15),
        "max_size": pick(None, cfg_section, "max_size", 500),
        "permutation_num": pick(None, cfg_section, "permutation_num", 1000),
        "weighting_exponent": pick(None, cfg_section, "weighting_exponent", 1),
        "seed": pick(None, cfg_section, "seed", 42)
    }
    log.info(f"GSEA 분석 파라미터: {gsea_params}")

    # --- 입력 데이터 준비 ---
    prerank_data, classic_data = None, None
    if mode == "prerank":
        prerank_input_csv = resolve_path(cli_path=None, cfg=cfg_all, config_key="prerank_input_csv", config_section=args.config_section)[0]
        df = pd.read_csv(prerank_input_csv)
        rank_metric_col = pick(None, cfg_section, "rank_metric_column", "log2fc")
        gene_symbol_col = pick(None, cfg_section, "gene_symbol_column", "gene")
        prerank_data = df[[gene_symbol_col, rank_metric_col]].dropna().sort_values(by=rank_metric_col, ascending=False)
    elif mode == "classic":
        expr_matrix_csv = resolve_path(cli_path=None, cfg=cfg_all, config_key="expression_matrix_csv", config_section=args.config_section)[0]
        class_labels_file = resolve_path(cli_path=None, cfg=cfg_all, config_key="class_labels_file", config_section=args.config_section)[0]
        expression_df = pd.read_csv(expr_matrix_csv, sep="\t")
        if 'NAME' in expression_df.columns:
            expression_df = expression_df.set_index('NAME').drop(columns=['DESCRIPTION'], errors='ignore')
        expression_df = expression_df.apply(pd.to_numeric, errors='coerce').fillna(0)
        classic_data = (expression_df, class_labels_file)

    # --- 최종 Excel 리포트 경로 설정 ---
    output_excel_path = resolve_path(cli_path=None, cfg=cfg_all, config_key="output_excel_file", config_section=args.config_section)[0]
    main_output_dir = Path(output_excel_path).parent / Path(output_excel_path).stem

    # --- 유전자 세트 리스트 순회 및 분석 실행 ---
    gene_sets_list = cfg_section.get("gene_sets", [])
    all_results = {}
    log.info(f"총 {len(gene_sets_list)}개의 유전자 세트에 대한 GSEA 스크리닝을 시작합니다.")

    # 이 스크립트 파일의 위치를 기준으로 프로젝트 루트를 안정적으로 찾습니다.
    # (src/analysis/gsea_analysis.py -> src/analysis -> src -> project_root)
    project_root = Path(__file__).resolve().parents[2]
    log.info(f"프로젝트 루트 경로를 '{project_root}'로 설정합니다.")

    for item in gene_sets_list:
        current_gene_set = str(item)
        if current_gene_set.endswith(".gmt"):
            # YAML에 적힌 상대 경로(예: 'ref/file.gmt')를
            # 프로젝트 루트 기준으로 절대 경로로 변환합니다.
            gmt_path = project_root / current_gene_set
            if not gmt_path.is_file():
                log.warning(f"경고: GMT 파일을 찾을 수 없습니다: '{gmt_path}'. 건너뜁니다.")
                continue
            current_gene_set = str(gmt_path)
        
        sheet_name = get_sheet_name(current_gene_set)
        sub_output_dir = main_output_dir / sheet_name
        
        result_df = None
        if mode == "prerank":
            result_df = run_gsea_prerank(prerank_data, current_gene_set, sub_output_dir, gsea_params)
        elif mode == "classic":
            result_df = run_gsea_classic(classic_data[0], classic_data[1], current_gene_set, sub_output_dir, gsea_params)

        if result_df is not None:
            all_results[sheet_name] = result_df

    # --- 모든 결과를 Excel 파일 하나로 통합 ---
    if all_results:
        write_results_to_excel(all_results, output_excel_path)
    else:
        log.warning("GSEA 분석이 성공적으로 완료되지 않아 생성된 결과가 없습니다.")

if __name__ == "__main__":
    _main()