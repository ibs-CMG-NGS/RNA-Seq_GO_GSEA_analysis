"""
I/O utility functions for reading and writing data files.

This module provides simple wrapper functions for common I/O operations
used throughout the RNA-Seq analysis pipeline.
"""
import pandas as pd
from typing import Dict, List


def read_excel_sheets(filepath: str, sheet_names: List[str]) -> Dict[str, pd.DataFrame]:
    """
    Read multiple sheets from an Excel file.
    
    Args:
        filepath: Path to the Excel file
        sheet_names: List of sheet names to read
        
    Returns:
        Dictionary mapping sheet names to their corresponding DataFrames
        
    Example:
        >>> sheets = read_excel_sheets("data.xlsx", ["Sheet1", "Sheet2"])
        >>> df1 = sheets["Sheet1"]
    """
    return {sheet: pd.read_excel(filepath, sheet_name=sheet) for sheet in sheet_names}


def save_dataframe(df: pd.DataFrame, path: str) -> None:
    """
    Save a DataFrame to CSV format without the index.
    
    Args:
        df: DataFrame to save
        path: Output file path
        
    Example:
        >>> df = pd.DataFrame({"gene": ["BRCA1", "TP53"], "log2fc": [1.5, -2.1]})
        >>> save_dataframe(df, "output.csv")
    """
    df.to_csv(path, index=False)
