"""
Core utility functions for RNA-Seq analysis pipeline.

This module provides commonly-used helper functions for file operations,
gene list management, data filtering, ID conversion, and basic visualizations.
It serves as a collection of reusable utilities used across the analysis pipeline.

Functions:
    ensure_outdir: Create output directories
    load_genes: Load and deduplicate gene lists
    read_excel_table: Read Excel files into DataFrames
    filter_genes_by_thresholds: Filter genes by statistical significance
    maybe_convert_ids: Convert gene IDs using MyGene service
    save_csv: Save DataFrames to CSV
    barplot: Create bar plots for enrichment results
    dotplot: Create dot plots for enrichment results
    volcano_plot: Create volcano plots for differential expression
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Optional, Tuple


def ensure_outdir(path: str) -> str:
    """
    Create a directory if it doesn't exist.
    
    Args:
        path: Directory path to create
        
    Returns:
        The same path (for chaining)
        
    Example:
        >>> output_dir = ensure_outdir("results/analysis1")
    """
    os.makedirs(path, exist_ok=True)
    return path

def load_genes(path: str, inline_genes: Optional[List[str]] = None) -> List[str]:
    """
    Load a list of gene symbols from a file or inline list, removing duplicates.
    
    Args:
        path: Path to a text file with one gene per line
        inline_genes: Optional list of genes to use instead of reading from file
        
    Returns:
        List of unique gene symbols in order of first appearance
        
    Example:
        >>> genes = load_genes("genes_of_interest.txt")
        >>> # Or provide genes directly:
        >>> genes = load_genes("", inline_genes=["BRCA1", "TP53", "BRCA1"])
        >>> len(genes)  # Duplicates removed
        2
    """
    if inline_genes:
        genes = [g.strip() for g in inline_genes if str(g).strip()]
    else:
        with open(path, "r") as f:
            genes = [line.strip() for line in f if line.strip()]
    seen = set()
    uniq = []
    for g in genes:
        if g not in seen:
            uniq.append(g); seen.add(g)
    return uniq

def read_excel_table(xlsx_path: str) -> pd.DataFrame:
    """
    Read an Excel file into a pandas DataFrame.
    
    Args:
        xlsx_path: Path to Excel file
        
    Returns:
        DataFrame containing the Excel data
    """
    return pd.read_excel(xlsx_path)

def filter_genes_by_thresholds(df: pd.DataFrame, gene_col: str, padj_col: str, 
                                log2fc_col: str, adj_p_cutoff: float, 
                                log2fc_cutoff: float, direction: str = "both") -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, List[str]]:
    """
    Filter genes based on statistical significance and fold change thresholds.
    
    Args:
        df: DataFrame containing gene expression data
        gene_col: Name of column containing gene symbols
        padj_col: Name of column containing adjusted p-values
        log2fc_col: Name of column containing log2 fold changes
        adj_p_cutoff: Adjusted p-value threshold (e.g., 0.05)
        log2fc_cutoff: Absolute log2 fold change threshold (e.g., 1.0)
        direction: Filter direction - "up", "down", or "both"
        
    Returns:
        Tuple of (filtered_df, up_regulated_df, down_regulated_df, gene_list)
        
    Example:
        >>> df = pd.DataFrame({
        ...     "gene": ["A", "B", "C"],
        ...     "log2fc": [2.0, -1.5, 0.5],
        ...     "padj": [0.001, 0.01, 0.1]
        ... })
        >>> filt, up, down, genes = filter_genes_by_thresholds(
        ...     df, "gene", "padj", "log2fc", 0.05, 1.0, "both"
        ... )
    """
    work = df.dropna(subset=[gene_col, padj_col, log2fc_col]).copy()
    work[padj_col] = pd.to_numeric(work[padj_col], errors="coerce")
    work[log2fc_col] = pd.to_numeric(work[log2fc_col], errors="coerce")
    work = work.dropna(subset=[padj_col, log2fc_col])

    sig = work[work[padj_col] <= adj_p_cutoff]
    up = sig[sig[log2fc_col] >= log2fc_cutoff]
    down = sig[sig[log2fc_col] <= -abs(log2fc_cutoff)]
    if direction == "up":
        filt = up
    elif direction == "down":
        filt = down
    else:
        filt = pd.concat([up, down], axis=0).drop_duplicates()

    genes = []
    seen = set()
    for g in filt[gene_col].astype(str).tolist():
        if g not in seen:
            genes.append(g); seen.add(g)
    return filt, up, down, genes

def maybe_convert_ids(genes: List[str], species: str, id_type: str) -> List[str]:
    """
    Convert gene IDs to gene symbols using the MyGene.info service.
    
    Attempts to convert various gene identifiers (Entrez ID, Ensembl, etc.)
    to standardized gene symbols. If MyGene is unavailable or conversion fails,
    returns the original gene list.
    
    Args:
        genes: List of gene identifiers to convert
        species: NCBI taxonomy ID (e.g., "9606" for human, "10090" for mouse)
        id_type: Type of input IDs - "symbol", "entrez", "ensembl", or "auto"
        
    Returns:
        List of gene symbols (converted or original if conversion fails)
        
    Example:
        >>> genes = ["7157", "672"]  # Entrez IDs
        >>> symbols = maybe_convert_ids(genes, species="9606", id_type="entrez")
        >>> # Returns: ["TP53", "BRCA1"]
        
    Note:
        Requires the mygene package to be installed. Falls back to original
        gene list if mygene is not available.
    """
    try:
        import mygene
    except Exception as e:
        print("[warn] mygene not available:", e); return genes
    mg = mygene.MyGeneInfo()
    scopes = {"symbol":"symbol","entrez":"entrezgene","ensembl":"ensembl.gene","auto":"symbol,entrezgene,ensembl.gene"}.get(id_type,"symbol")
    if not genes: return []
    res = mg.querymany(genes, scopes=scopes, fields="symbol", species=species, as_dataframe=False, returnall=False)
    out = []
    for x in res:
        if isinstance(x, dict) and "symbol" in x: out.append(x["symbol"])
        elif isinstance(x, dict) and "query" in x: out.append(str(x["query"]))
    out = [g for g in out if g]
    uniq = []; seen=set()
    for g in out:
        if g not in seen: uniq.append(g); seen.add(g)
    return uniq

def save_csv(df: pd.DataFrame, path: str) -> None:
    """
    Save DataFrame to CSV and print confirmation message.
    
    Args:
        df: DataFrame to save
        path: Output file path
    """
    df.to_csv(path, index=False)
    print(f"[ok] wrote {path}")

def barplot(enr_res2d: pd.DataFrame, out_png: str, top_terms: int = 20, 
            title: str = "GO Enrichment (Top)") -> None:
    """
    Create a horizontal bar plot for enrichment analysis results.
    
    Args:
        enr_res2d: Enrichment results DataFrame with "Term", "Adjusted P-value", 
                   and "Combined Score" columns
        out_png: Output PNG file path
        top_terms: Number of top terms to display
        title: Plot title
        
    Example:
        >>> results = pd.DataFrame({
        ...     "Term": ["pathway1", "pathway2"],
        ...     "Adjusted P-value": [0.001, 0.01],
        ...     "Combined Score": [50, 30]
        ... })
        >>> barplot(results, "enrichment_bar.png", top_terms=10)
    """
    df = enr_res2d.sort_values("Adjusted P-value").head(top_terms).copy()
    if df.empty:
        print("[warn] barplot skipped: empty results"); return
    plt.figure(figsize=(10,6))
    plt.barh(df["Term"][::-1], df["Combined Score"][::-1])
    plt.xlabel("Combined Score")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(out_png, dpi=150, bbox_inches="tight"); plt.close()
    print(f"[ok] wrote {out_png}")

def dotplot(enr_res2d: pd.DataFrame, out_png: str, top_terms: int = 20, 
            title: str = "GO Enrichment (Top)") -> None:
    """
    Create a dot plot for enrichment analysis results.
    
    Dot size represents the overlap ratio (genes in term / total genes in term).
    
    Args:
        enr_res2d: Enrichment results DataFrame with "Term", "Adjusted P-value", 
                   and "Overlap" columns
        out_png: Output PNG file path
        top_terms: Number of top terms to display
        title: Plot title
        
    Example:
        >>> results = pd.DataFrame({
        ...     "Term": ["pathway1", "pathway2"],
        ...     "Adjusted P-value": [0.001, 0.01],
        ...     "Overlap": ["10/50", "5/30"]
        ... })
        >>> dotplot(results, "enrichment_dot.png", top_terms=10)
    """
    df = enr_res2d.sort_values("Adjusted P-value").head(top_terms).copy()
    if df.empty:
        print("[warn] dotplot skipped: empty results"); return
    ratios = []
    for s in df["Overlap"]:
        try:
            num, den = s.split("/"); ratios.append(float(num)/float(den))
        except Exception:
            ratios.append(0.0)
    df["overlap_ratio"] = ratios
    plt.figure(figsize=(10,6))
    plt.scatter(df["Adjusted P-value"], range(len(df)), s=(df["overlap_ratio"]*400)+10)
    plt.yticks(range(len(df)), df["Term"])
    plt.gca().invert_yaxis()
    plt.xlabel("Adjusted P-value")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(out_png, dpi=150, bbox_inches="tight"); plt.close()
    print(f"[ok] wrote {out_png}")

def volcano_plot(df: pd.DataFrame, log2fc_col: str, padj_col: str, out_png: str, 
                 log2fc_cutoff: float, adj_p_cutoff: float) -> None:
    """
    Create a volcano plot for differential expression analysis.
    
    Plots log2 fold change vs -log10(adjusted p-value) with threshold lines.
    
    Args:
        df: DataFrame with expression data
        log2fc_col: Name of log2 fold change column
        padj_col: Name of adjusted p-value column
        out_png: Output PNG file path
        log2fc_cutoff: Fold change threshold for significance lines
        adj_p_cutoff: P-value threshold for horizontal line
        
    Example:
        >>> df = pd.DataFrame({
        ...     "log2fc": [2.0, -1.5, 0.5, -3.0],
        ...     "padj": [0.001, 0.01, 0.1, 0.0001]
        ... })
        >>> volcano_plot(df, "log2fc", "padj", "volcano.png", 1.0, 0.05)
    """
    import numpy as np
    work = df.dropna(subset=[log2fc_col, padj_col]).copy()
    work[log2fc_col] = pd.to_numeric(work[log2fc_col], errors="coerce")
    work[padj_col] = pd.to_numeric(work[padj_col], errors="coerce")
    work = work.dropna(subset=[log2fc_col, padj_col])
    work["neglog10_padj"] = -np.log10(work[padj_col].clip(lower=1e-300))
    plt.figure(figsize=(7,5))
    plt.scatter(work[log2fc_col], work["neglog10_padj"])
    y_thr = -np.log10(adj_p_cutoff if adj_p_cutoff>0 else 1e-300)
    plt.axhline(y=y_thr)
    plt.axvline(x=log2fc_cutoff)
    plt.axvline(x=-abs(log2fc_cutoff))
    plt.xlabel("log2FC"); plt.ylabel("-log10(adj p-value)")
    plt.title("Volcano plot")
    plt.tight_layout()
    plt.savefig(out_png, dpi=150, bbox_inches="tight"); plt.close()
    print(f"[ok] wrote {out_png}")
