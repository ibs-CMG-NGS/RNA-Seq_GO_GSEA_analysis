#!/usr/bin/env python3
import gseapy as gp
import pandas as pd

# Load expression matrix with NAME as string
expr_df = pd.read_csv("results/batch_gsea_H2O2_GABA/H2O2-treated/gsea_expression_matrix.txt", sep="\t", dtype={"NAME": str, "DESCRIPTION": str})
expr_df = expr_df.set_index('NAME').drop(columns=['DESCRIPTION'], errors='ignore')

# Ensure index is string BEFORE numeric conversion
expr_df.index = expr_df.index.astype(str)

# Now convert columns to numeric
expr_df = expr_df.apply(pd.to_numeric, errors='coerce').fillna(0)

# Print index types
print("Expression matrix shape:", expr_df.shape)
print("Expression matrix columns:", list(expr_df.columns))
print("Index dtype:", expr_df.index.dtype)
print("First 5 index values:", list(expr_df.index[:5]))
print("Index value types:", [type(x) for x in expr_df.index[:5]])

# Class labels file
cls_file = "results/batch_gsea_H2O2_GABA/H2O2-treated/gsea_class_labels.cls"

print("\nClass labels file content:")
with open(cls_file) as f:
    print(f.read())

# Try running GSEA
print("\nRunning Classic GSEA...")
try:
    results = gp.gsea(
        data=expr_df,
        gene_sets="KEGG_2021_Mouse",
        cls=cls_file,
        outdir="test_gsea",
        min_size=15,
        max_size=500,
        permutation_num=100,  # 적은 수로 빠르게 테스트
        seed=42,
        verbose=True
    )
    print("\n✅ SUCCESS! Results shape:", results.res2d.shape)
    print(results.res2d.head())
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
