"""
Setup script for RNA-Seq GO/GSEA Analysis Pipeline

This allows the package to be installed with:
    pip install -e .  (development mode)
    pip install .     (regular installation)
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read the README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = [
        line.strip() 
        for line in requirements_file.read_text(encoding="utf-8").split("\n")
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="rnaseq-go-gsea-analysis",
    version="1.0.0",
    author="RNA-Seq Analysis Team",
    author_email="",
    description="A modular pipeline for RNA-Seq post-analysis focusing on GO and GSEA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ibs-CMG-NGS/RNA-Seq_GO_GSEA_analysis",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    dependency_links=[
        "git+https://github.com/parkgilbong/YG_utils_analysis.git@main#egg=YG_utils_analysis"
    ],
    entry_points={
        "console_scripts": [
            "rnaseq-data-load=analysis.data_loading:_main",
            "rnaseq-filter=analysis.filtering:_main",
            "rnaseq-volcano=analysis.volcano:_main",
            "rnaseq-go-enrich=analysis.go_enrich:_main",
            "rnaseq-go-barplot=analysis.go_barplot:_main",
            "rnaseq-gsea=analysis.gsea_analysis:_main",
            "rnaseq-gsea-plot=analysis.gsea_plot:_main",
            "rnaseq-report=analysis.report_generation:_main",
            "rnaseq-batch=analysis.batch_runner:_main",
        ],
    },
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=3.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.950",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
