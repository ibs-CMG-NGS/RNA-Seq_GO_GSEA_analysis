# Workflow Execution Method Comparison

This guide helps you choose the best execution method for your RNA-Seq analysis needs.

## Quick Decision Guide

```
┌─────────────────────────────────────────┐
│ How many samples do you need to process?│
└─────────────────────────────────────────┘
                    │
        ┌───────────┴──────────┐
        │                      │
    1-2 samples          3+ samples
        │                      │
        ▼                      ▼
   ┌─────────┐          ┌──────────┐
   │ Single  │          │  Batch   │
   │ Sample  │          │Processing│
   └─────────┘          └──────────┘
        │                      │
        │              ┌───────┴────────┐
        │              │                │
        │         Sequential?     Parallel?
        │              │                │
        │              ▼                ▼
        │         ┌─────────┐    ┌──────────┐
        │         │ Python  │    │Snakemake │
        │         │ Batch   │    │(Recommend)│
        │         │ Runner  │    └──────────┘
        │         └─────────┘
        │
   ┌────┴─────┐
   │          │
Learning?  Production?
   │          │
   ▼          ▼
Notebook    CLI/Snakemake
```

## Detailed Comparison

| Feature | Jupyter Notebook | CLI Tools | Python batch_runner.py | Snakemake |
|---------|-----------------|-----------|------------------------|-----------|
| **Learning Curve** | Easy | Medium | Medium | Medium-Hard |
| **Interactivity** | ✅ High | ❌ None | ❌ None | ❌ None |
| **Batch Processing** | ❌ Manual | ⚠️ Manual | ✅ Auto | ✅ Auto |
| **Parallelization** | ❌ No | ❌ No | ❌ No | ✅ Yes |
| **Error Recovery** | ⚠️ Manual | ⚠️ Manual | ⚠️ Manual | ✅ Auto |
| **Reproducibility** | ⚠️ Medium | ✅ High | ✅ High | ✅ Highest |
| **HPC Compatible** | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes (Best) |
| **Speed (4 samples)** | Slow | Slow | ~120 min | ~35 min |
| **Best For** | Exploration | Single runs | Simple batches | Large batches |

## Use Case Recommendations

### Use Jupyter Notebooks When:
- 🎓 Learning the pipeline
- 🔬 Exploring one sample in detail
- 📊 Need to visualize intermediate results
- 🛠️ Testing different parameters interactively
- 📝 Creating analysis reports with explanations

**Example**:
```bash
jupyter notebook
# Open notebooks/GO_Pipeline.ipynb
```

### Use CLI Tools When:
- 🎯 Running single analysis step
- 🔄 Re-running specific step with different parameters
- 🐞 Debugging pipeline issues
- 📋 Creating custom workflows
- 🖥️ Integrating into existing scripts

**Example**:
```bash
python src/analysis/filtering.py \
  --config configs/GO_pipeline.yaml \
  --config-section filtering \
  --padj-cutoff 0.01
```

### Use Python batch_runner.py When:
- 📦 Processing 2-5 samples
- 💻 Limited computing resources (single core)
- 🚫 Cannot install Snakemake
- ⚡ Need simple, sequential execution
- 📁 Have existing manifest files

**Example**:
```bash
python src/analysis/batch_runner.py \
  --manifest configs/batch_manifest.yaml
```

### Use Snakemake When:
- 🚀 Processing 5+ samples
- 💪 Have multi-core system or HPC access
- ⚡ Need maximum speed
- 🔄 Want automatic error recovery
- 📊 Need workflow visualization
- 🏢 Production environment
- 🔬 Large-scale studies

**Example**:
```bash
snakemake --snakefile workflow/Snakefile_batch_GO \
  --configfile workflow/config/batch_go_config.yaml \
  --cores 8
```

## Performance Benchmarks

### Single Sample Analysis
All methods are similar for single samples:

| Method | Time | Complexity |
|--------|------|------------|
| Notebook | ~30 min | Low |
| CLI | ~30 min | Low |
| Snakemake | ~30 min | Medium |

**Recommendation**: Use notebooks for exploration, CLI for automation

### Batch Processing (4 Samples)

| Method | Sequential Time | Parallel Time | Setup Effort |
|--------|----------------|---------------|--------------|
| Notebook | ~120 min | N/A | Low |
| CLI Scripts | ~120 min | N/A | Medium |
| Python batch_runner | ~120 min | N/A | Low |
| Snakemake (4 cores) | ~120 min | **~35 min** | Medium |

**Performance Gain**: **3.4x faster** with Snakemake on 4 cores

### Large Batch Processing (20 Samples)

| Method | Sequential Time | Parallel Time (HPC) | Scalability |
|--------|----------------|---------------------|-------------|
| Python batch_runner | ~600 min | N/A | Poor |
| Snakemake (8 cores) | ~600 min | **~80 min** | Excellent |
| Snakemake (HPC cluster) | ~600 min | **~35 min** | Excellent |

**Performance Gain**: **Up to 17x faster** with Snakemake on HPC

## Resource Requirements

### Memory Usage

| Method | Memory per Sample | Total Memory |
|--------|-------------------|--------------|
| Notebook | 2-4 GB | 2-4 GB |
| CLI | 2-4 GB | 2-4 GB |
| Python batch_runner | 2-4 GB | 2-4 GB |
| Snakemake (4 parallel) | 2-4 GB | 8-16 GB |

### CPU Usage

| Method | CPU per Sample | Total CPU Usage |
|--------|----------------|-----------------|
| Notebook | 1 core | 1 core |
| CLI | 1 core | 1 core |
| Python batch_runner | 1 core | 1 core |
| Snakemake | 1 core | Up to N cores |

## Learning Path

### For Beginners
1. ✅ Start with Jupyter notebooks (`notebooks/GO_Pipeline.ipynb`)
2. ✅ Try CLI tools for single steps
3. ✅ Use Python batch_runner for 2-3 samples
4. ✅ Graduate to Snakemake for larger projects

### For Experienced Users
1. ✅ Jump straight to Snakemake
2. ✅ Use helper scripts (`workflow/scripts/run_snakemake_go.sh`)
3. ✅ Customize configs in `workflow/config/`
4. ✅ Deploy to HPC for large-scale analyses

### For HPC Users
1. ✅ Setup Snakemake environment
2. ✅ Test locally with dry-run
3. ✅ Deploy to cluster with `--cluster` option
4. ✅ Monitor with Snakemake logging

## Migration Strategy

If you're currently using Python batch_runner.py:

### Phase 1: Parallel Testing
- Continue using batch_runner.py for production
- Test Snakemake on small subset
- Compare results to ensure equivalence

### Phase 2: Gradual Adoption
- Use Snakemake for new projects
- Migrate existing configs to workflow/config/
- Build confidence with workflow execution

### Phase 3: Full Migration
- Switch all batch processing to Snakemake
- Keep batch_runner.py as backup
- Train team on Snakemake usage

## Troubleshooting

### "Which method should I use for my thesis project?"
→ **Notebooks** for exploration + **Snakemake** for final batch processing

### "I only have a laptop with 2 cores"
→ **Python batch_runner** or **Snakemake with --cores 2**

### "I need to process 50 samples on HPC"
→ **Snakemake with --cluster** (definitely!)

### "I'm new to command line"
→ Start with **Jupyter notebooks**

### "I need reproducible results for publication"
→ **Snakemake** (provides full provenance tracking)

## Summary

Choose your method based on:

- **Sample Count**: More samples → More benefit from Snakemake
- **Resources**: More cores → More benefit from Snakemake  
- **Experience**: Learning → Notebooks, Production → Snakemake
- **Environment**: HPC access → Snakemake is essential
- **Timeline**: Time-critical → Snakemake for speed

**General Rule**: 
- 1-2 samples: Any method works
- 3-10 samples: Python batch_runner or Snakemake
- 10+ samples: Snakemake strongly recommended
- HPC environment: Always use Snakemake

## Quick Start Commands

```bash
# Exploration (1 sample)
jupyter notebook notebooks/GO_Pipeline.ipynb

# Simple batch (2-5 samples)
python src/analysis/batch_runner.py --manifest configs/my_batch.yaml

# Efficient batch (5+ samples)
snakemake --snakefile workflow/Snakefile_batch_GO \
  --configfile workflow/config/batch_go_config.yaml \
  --cores 4

# HPC cluster (10+ samples)
snakemake --snakefile workflow/Snakefile_batch_GO \
  --configfile workflow/config/batch_go_config.yaml \
  --cluster "sbatch --time=02:00:00 --mem=16G" \
  --jobs 10
```
