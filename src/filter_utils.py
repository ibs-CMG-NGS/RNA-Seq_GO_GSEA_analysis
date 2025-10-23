import pandas as pd
from typing import List

def filter_genes(df: pd.DataFrame, gene_list: List[str], gene_col: str = "gene") -> pd.DataFrame:
    """
    Filters a DataFrame based on a given list of genes.

    Args:
        df (pd.DataFrame): The input DataFrame.
        gene_list (List[str]): A list of gene names to filter by.
        gene_col (str, optional): The name of the column containing gene names. Defaults to "gene".
    """
    return df[df[gene_col].isin(gene_list)].copy()
