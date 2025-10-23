"""
Gene filtering utilities for RNA-Seq analysis.

This module provides functions for filtering gene expression data
based on gene lists or other criteria.
"""
import pandas as pd
from typing import List


def filter_genes(df: pd.DataFrame, gene_list: List[str], gene_col: str = "gene") -> pd.DataFrame:
    """
    Filter a DataFrame to include only genes present in a specified gene list.
    
    This is useful for focusing analysis on genes of interest, such as genes
    from a specific pathway or previously identified candidate genes.

    Args:
        df: Input DataFrame containing gene expression data
        gene_list: List of gene names/symbols to keep
        gene_col: Name of the column containing gene identifiers. Defaults to "gene"
        
    Returns:
        A new DataFrame containing only rows where the gene column value
        is present in the gene_list
        
    Example:
        >>> df = pd.DataFrame({"gene": ["BRCA1", "TP53", "EGFR"], "log2fc": [1.5, -2.1, 0.8]})
        >>> genes_of_interest = ["BRCA1", "TP53"]
        >>> filtered = filter_genes(df, genes_of_interest)
        >>> len(filtered)
        2
    """
    return df[df[gene_col].isin(gene_list)].copy()
