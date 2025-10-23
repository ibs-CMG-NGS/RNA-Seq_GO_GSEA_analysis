# Contributing to RNA-Seq GO/GSEA Analysis Pipeline

Thank you for your interest in contributing to this project! This document provides guidelines and best practices for contributing.

## 🎯 Project Philosophy

This project follows several key principles:

1. **Modularity:** Each analysis step is an independent, reusable module
2. **CLI-First Design:** Every module is a complete command-line tool
3. **Configuration over Code:** Use YAML configs for parameters, not hardcoding
4. **Documentation:** Code should be self-documenting with comprehensive docstrings
5. **Reproducibility:** Same inputs + same config = same outputs

## 🚀 Getting Started

### Setting Up Development Environment

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/RNA-Seq_GO_GSEA_analysis.git
cd RNA-Seq_GO_GSEA_analysis

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
pip install git+https://github.com/parkgilbong/YG_utils_analysis.git@main

# Install development dependencies
pip install pytest pytest-cov black flake8 mypy
```

### Running Tests

```bash
# Run all tests (when implemented)
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_filtering.py
```

## 📝 Code Style Guidelines

### Python Code Style

We follow PEP 8 with some project-specific conventions:

```python
# Good: Type hints for all function parameters and returns
def filter_genes(df: pd.DataFrame, genes: List[str], 
                 gene_col: str = "gene") -> pd.DataFrame:
    """
    Filter DataFrame to include only specified genes.
    
    Args:
        df: Input DataFrame
        genes: List of gene symbols to keep
        gene_col: Name of gene column
        
    Returns:
        Filtered DataFrame
        
    Example:
        >>> df = pd.DataFrame({"gene": ["A", "B"], "value": [1, 2]})
        >>> filtered = filter_genes(df, ["A"])
    """
    return df[df[gene_col].isin(genes)].copy()

# Bad: No type hints, no docstring, unclear variable names
def filter_genes(d, g, c="gene"):
    return d[d[c].isin(g)].copy()
```

### Docstring Format

Use NumPy/Google style docstrings with these sections:

```python
def my_function(arg1: str, arg2: int = 10) -> bool:
    """
    Short one-line description.
    
    Longer description explaining what the function does,
    any important details, and usage context.
    
    Args:
        arg1: Description of first argument
        arg2: Description of second argument with default
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When input is invalid
        
    Example:
        >>> result = my_function("test", 20)
        >>> print(result)
        True
        
    Note:
        Any important notes or warnings for users.
    """
    pass
```

### Module Structure

Each analysis module should follow this pattern:

```python
"""
Module-level docstring explaining purpose.

Functions:
    - helper_function1: Brief description
    - helper_function2: Brief description
    - _parse_args: CLI argument parsing
    - _main: Main entry point
"""
import argparse
import logging
from pathlib import Path
from typing import List, Optional

# Import utilities
from utils.config_utils import get_cfg, resolve_path

# Setup logging
logging, _ = setup_logging()


def helper_function(param: str) -> int:
    """Do something useful."""
    pass


def _parse_args(argv=None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Module description")
    parser.add_argument("--config", help="Config file path")
    # ... more arguments
    return parser.parse_args(argv)


def _main(argv=None) -> None:
    """Main entry point for CLI."""
    args = _parse_args(argv)
    # Implementation
    pass


if __name__ == "__main__":
    _main()
```

## 🔧 Making Changes

### Adding a New Analysis Module

1. **Create the module file** in `src/analysis/`
2. **Follow the module structure** shown above
3. **Add CLI arguments** using argparse
4. **Support YAML configuration** via `get_cfg()` and `resolve_path()`
5. **Add to batch runner** in `STEP_SCRIPT_MAP` if appropriate
6. **Document in README** with usage examples
7. **Add tests** (when test infrastructure exists)

### Modifying Existing Modules

1. **Maintain backward compatibility** when possible
2. **Update docstrings** to reflect changes
3. **Update configuration examples** in `configs/`
4. **Test with existing config files** to ensure they still work
5. **Update README** if user-facing behavior changes

### Adding Utility Functions

1. **Place in appropriate module:**
   - `src/utils.py` - Core utilities used across modules
   - `src/io_utils.py` - File I/O operations
   - `src/filter_utils.py` - Gene filtering operations
   - `src/viz_utils.py` - Visualization functions
2. **Add comprehensive docstrings** with examples
3. **Use type hints** for all parameters and returns
4. **Keep functions focused** - one function, one purpose

## 🧪 Testing Best Practices

When adding tests:

```python
import pytest
import pandas as pd
from src.filter_utils import filter_genes


def test_filter_genes_basic():
    """Test basic gene filtering functionality."""
    df = pd.DataFrame({
        "gene": ["BRCA1", "TP53", "EGFR"],
        "log2fc": [1.5, -2.0, 0.8]
    })
    genes_to_keep = ["BRCA1", "TP53"]
    
    result = filter_genes(df, genes_to_keep)
    
    assert len(result) == 2
    assert set(result["gene"]) == {"BRCA1", "TP53"}


def test_filter_genes_empty_list():
    """Test filtering with empty gene list."""
    df = pd.DataFrame({"gene": ["A", "B"], "value": [1, 2]})
    result = filter_genes(df, [])
    assert len(result) == 0


def test_filter_genes_custom_column():
    """Test filtering with custom gene column name."""
    df = pd.DataFrame({"symbol": ["A", "B"], "value": [1, 2]})
    result = filter_genes(df, ["A"], gene_col="symbol")
    assert len(result) == 1
```

## 📚 Documentation

### Updating README

When adding features:
- Add to relevant section (Quick Start, Usage Guide, CLI Reference)
- Provide concrete examples
- Update project structure if adding new files/directories

### Adding Examples

When documenting:
- Use **realistic biological examples** when possible
- Show **complete workflows**, not just individual commands
- Include **expected output** descriptions
- Add **troubleshooting tips** for common issues

## 🐛 Reporting Bugs

When filing an issue:

1. **Use a clear, descriptive title**
2. **Describe the expected vs. actual behavior**
3. **Provide reproduction steps:**
   ```
   1. Run command X with config Y
   2. Observe error Z
   ```
4. **Include version information:**
   - Python version
   - Operating system
   - Package versions (`pip list`)
5. **Attach relevant files** (config, logs, error messages)
6. **Sanitize sensitive data** before sharing

## 💡 Suggesting Features

When proposing new features:

1. **Explain the use case** - What problem does it solve?
2. **Describe the proposed solution** - How should it work?
3. **Consider alternatives** - Are there other approaches?
4. **Discuss impact** - How does it fit with existing features?

## 📋 Pull Request Process

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Make your changes:**
   - Follow code style guidelines
   - Add/update docstrings
   - Add/update tests
   - Update documentation

3. **Test your changes:**
   ```bash
   # Run linting
   flake8 src/
   
   # Run type checking
   mypy src/
   
   # Run tests
   pytest tests/
   
   # Test with actual config files
   python src/analysis/your_module.py --config configs/test_config.yaml
   ```

4. **Commit with clear messages:**
   ```bash
   git commit -m "Add feature: improved volcano plot annotations"
   ```

5. **Push and create pull request:**
   ```bash
   git push origin feature/my-new-feature
   ```

6. **PR Description should include:**
   - What changes were made
   - Why the changes were necessary
   - How to test the changes
   - Any breaking changes
   - Related issues

## ✅ Review Checklist

Before submitting a PR, verify:

- [ ] Code follows project style guidelines
- [ ] All functions have comprehensive docstrings
- [ ] Type hints are used throughout
- [ ] No debugging print statements (use logging instead)
- [ ] Configuration-based, not hardcoded values
- [ ] Backward compatible or breaking changes documented
- [ ] README updated if user-facing changes
- [ ] Examples provided for new features
- [ ] Tests pass (when test infrastructure exists)
- [ ] Manual testing performed with real data

## 🤝 Code Review Guidelines

When reviewing PRs:

- **Be constructive** - Suggest improvements, don't just criticize
- **Explain reasoning** - Help others learn
- **Consider alternatives** - There may be multiple valid approaches
- **Test the changes** - Don't just read the code
- **Check documentation** - Is it clear and complete?

## 📞 Getting Help

- **Questions:** Open a GitHub Discussion
- **Issues:** File a GitHub Issue
- **General Chat:** Use project communication channels

## 🙏 Recognition

Contributors will be:
- Listed in project contributors
- Credited in release notes
- Acknowledged in documentation

Thank you for contributing to making RNA-Seq analysis more accessible and reproducible!
