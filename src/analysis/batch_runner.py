# =================================
# file: src/batch_runner.py
# =================================
# This module provides a batch processing script to run the entire RNA-Seq analysis pipeline for multiple samples.
# It reads a manifest YAML file that defines the samples and any sample-specific configuration overrides.
# For each sample, it merges a base configuration with the overrides and executes each analysis step sequentially.
#
# The pipeline steps to be executed are also defined in the manifest file, allowing for flexible execution.
#
# Functions
# ---------
# - deep_merge(base_dict: dict, override_dict: dict) -> dict:
#     Recursively merges two dictionaries.
# - run_command(command: list, temp_config_path: str) -> None:
#     Executes an analysis script as a subprocess with a temporary configuration file.
# - _parse_args() -> argparse.Namespace:
#     Parses the command-line argument for the manifest file path.
# - _main() -> None:
#     The main entry point. It reads the manifest, iterates through samples, generates temporary configurations, and executes the defined pipeline steps.
#
# Usage
# -----
# Run as a script to execute the batch analysis defined in a manifest file:
#     python src/batch_runner.py --manifest configs/batch_manifest.yaml
#
# Dependencies
# ------------
# - PyYAML, argparse, copy, logging, os, subprocess, sys, datetime, pathlib
import argparse
import copy
import logging
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import yaml

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [%(name)s] - %(message)s')

# Maps step names from the manifest to their corresponding script paths.
# Now stores a tuple: (script_path, config_section_name)
STEP_SCRIPT_MAP = {
    "data_loading": ("src/analysis/data_loading.py", "data_loading"),
    "filtering": ("src/analysis/filtering.py", "filtering"),
    "volcano": ("src/analysis/volcano.py", "volcano"),
    "go_enrich": ("src/analysis/go_enrich.py", "go_enrich"),
    "go_barplot": ("src/analysis/go_barplot.py", "go_barplot"),
    "gsea_analysis": ("src/analysis/gsea_analysis.py", "gsea"),
    "gsea_plot": ("src/analysis/gsea_plot.py", "gsea_plot"), 
    "compare_degs": ("src/analysis/compare_degs.py", "deg_comparison"),
    "report_generation": ("src/analysis/report_generation.py", "report"),
}


def deep_merge(base_dict, override_dict):
    """
    Recursively merges two dictionaries. Values in override_dict take precedence.
    """
    result = copy.deepcopy(base_dict)
    for key, value in override_dict.items():
        if isinstance(value, dict) and key in result and isinstance(result[key], dict):
            result[key] = deep_merge(result[key], value)
        # If the override value is not a dictionary, but the base value for the same key is, we assume a shorthand override.
        # This handles cases like `data_loading: "path/to/excel.xlsx"` in the manifest,
        # where the base config's `data_loading` is a dictionary.
        elif key in result and isinstance(result[key], dict) and not isinstance(value, dict):
            # This handles cases like `data_loading: "path/to/excel.xlsx"` in the manifest,
            # where the base config's `data_loading` is a dictionary.
            # Heuristic: The override value should replace the value of the *first* key in the base dictionary.
            # e.g., for `data_loading`, this would be `excel_path`.
            if result[key]:  # Ensure the dictionary is not empty
                first_key = next(iter(result[key]))
                result[key][first_key] = value
        else:
            result[key] = value
    return result


def run_command(command, temp_config_path, config_section):
    """
    Executes a shell command and logs its execution.
    """
    # Add the config argument to the command
    full_command = command + ["--config", str(temp_config_path), "--config-section", config_section]
    
    script_name = Path(full_command[1]).name
    log = logging.getLogger(script_name)
    
    log.info(f"Executing: {' '.join(full_command)}")
    try:
        # We use shell=True on Windows to correctly resolve python executable without full path
        # On Linux/macOS, shell=False with a list of args is safer.
        is_windows = sys.platform == "win32"
        result = subprocess.run(
            ' '.join(full_command) if is_windows else full_command,
            check=True,
            capture_output=True,
            text=True,
            shell=is_windows,
            encoding='utf-8'
        )
        if result.stdout:
            log.info(f"Output:\n{result.stdout}")
        if result.stderr:
            log.warning(f"Stderr:\n{result.stderr}")
        log.info("Execution successful.")
    except subprocess.CalledProcessError as e:
        log.error(f"Execution failed with return code {e.returncode}.")
        log.error(f"Command: {' '.join(e.cmd)}")
        log.error(f"Stdout:\n{e.stdout}")
        log.error(f"Stderr:\n{e.stderr}")
        # Stop the batch process for the current sample if a step fails
        raise


def _parse_args(argv=None):
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Batch runner for the RNA-Seq analysis pipeline.")
    parser.add_argument(
        "--manifest",
        required=True,
        help="Path to the batch manifest YAML file (e.g., 'configs/batch_manifest.yaml')."
    )
    return parser.parse_args(argv)


def _main(argv=None):
    """Main entry point for the batch runner script."""
    args = _parse_args(argv)
    
    # The script is in src/analysis, so the project root is 2 levels up.
    project_root = Path(__file__).resolve().parents[2]
    manifest_path = project_root / args.manifest

    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = yaml.safe_load(f)

    base_config_path = project_root / manifest['base_config_path']
    with open(base_config_path, 'r', encoding='utf-8') as f:
        base_config = yaml.safe_load(f)

    # Create a root directory for this batch run with a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    batch_output_root_str = manifest.get("output_root", "results/batch_run_{timestamp}").format(timestamp=timestamp)
    batch_output_root = project_root / batch_output_root_str
    batch_output_root.mkdir(parents=True, exist_ok=True)
    logging.info(f"Batch output root: {batch_output_root}")

    for i, sample in enumerate(manifest['samples']):
        sample_name = sample['name']
        logging.info(f"--- Processing sample {i+1}/{len(manifest['samples'])}: {sample_name} ---")

        # Create a specific config for this sample by merging base and overrides
        sample_config = deep_merge(base_config, sample.get('overrides', {}))
        
        # --- Dynamically set the output directory for this sample ---
        # This ensures each sample's results are in a separate subfolder.
        # It overrides any ROOT_DIR from the manifest or base config.
        sample_output_dir = batch_output_root / sample_name
        sample_config['ROOT_DIR'] = str(sample_output_dir.relative_to(project_root))

        # Create a temporary config file for the current sample
        temp_config_path = batch_output_root / f"temp_config_{sample_name}.yaml"
        with open(temp_config_path, 'w', encoding='utf-8') as f:
            yaml.dump(sample_config, f, default_flow_style=False, sort_keys=False)
        
        logging.info(f"Generated temporary config for '{sample_name}' at: {temp_config_path}")

        # Execute each step of the pipeline
        try:
            for step_name in manifest.get('pipeline_steps', []):
                if step_name not in STEP_SCRIPT_MAP:
                    logging.warning(f"Skipping unknown pipeline step: {step_name}")
                    continue
                script_path_str, config_section = STEP_SCRIPT_MAP[step_name] 
                script_path = project_root / script_path_str
                command = ["python", str(script_path)]
                run_command(command, temp_config_path, config_section)
        except subprocess.CalledProcessError:
            logging.error(f"Pipeline failed for sample '{sample_name}'. Moving to the next sample.")
            continue # Continue to the next sample

    logging.info("--- Batch processing complete. ---")

if __name__ == "__main__":
    _main()
