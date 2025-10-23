
import os
import pandas as pd
import matplotlib.pyplot as plt

def ensure_outdir(path: str):
    os.makedirs(path, exist_ok=True)
    return path

def load_genes(path: str, inline_genes=None):
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

def read_excel_table(xlsx_path: str):
    return pd.read_excel(xlsx_path)

def filter_genes_by_thresholds(df, gene_col, padj_col, log2fc_col, adj_p_cutoff, log2fc_cutoff, direction="both"):
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

def maybe_convert_ids(genes, species: str, id_type: str):
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

def save_csv(df, path):
    df.to_csv(path, index=False)
    print(f"[ok] wrote {path}")

def barplot(enr_res2d, out_png, top_terms=20, title="GO Enrichment (Top)"):
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

def dotplot(enr_res2d, out_png, top_terms=20, title="GO Enrichment (Top)"):
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

def volcano_plot(df, log2fc_col, padj_col, out_png, log2fc_cutoff, adj_p_cutoff):
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
