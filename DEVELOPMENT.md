# Development Guide

This guide provides detailed instructions for developers who want to contribute to or work with the CityBike Analytics Platform.

## Table of Contents

- [Development Environment](#development-environment)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Code Quality Tools](#code-quality-tools)
- [Running Tests](#running-tests)
- [Common Tasks](#common-tasks)
- [Troubleshooting](#troubleshooting)

## Development Environment

### System Requirements

- **Python:** 3.8 or higher
- **Git:** Latest version
- **Virtual Environment:** venv or conda
- **Operating System:** Windows, macOS, or Linux

### Recommended Tools

- **IDE:** VS Code with Python extension
- **Code Formatter:** Black
- **Linter:** Pylint, Flake8
- **Type Checker:** mypy
- **Test Framework:** pytest
- **Pre-commit Hooks:** pre-commit

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/mutabazi105/citybike-capstone.git
cd citybike-capstone
```

### 2. Create Virtual Environment

**Windows:**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Mac/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
# Core dependencies
pip install -r requirements.txt

# Development dependencies
pip install black pylint mypy pytest pytest-cov pytest-xdist
pip install pre-commit
```

### 4. Setup Pre-commit Hooks (Optional but Recommended)

```bash
pre-commit install
```

This will automatically run quality checks before each commit!

### 5. Verify Installation

```bash
# Run the main pipeline
python -m citybike.main

# Run tests
pytest

# Check code quality
black --check citybike/
pylint citybike/
mypy citybike/
```

## Project Structure

```
citybike-capstone/
│
├── citybike/                      # Main package
│   ├── __init__.py               # Package initialization
│   ├── models.py                 # Domain models (OOP)
│   ├── factories.py              # Factory Pattern
│   ├── pricing.py                # Strategy Pattern
│   ├── algorithms.py             # Sorting/Searching
│   ├── numerical.py              # NumPy operations
│   ├── analyzer.py               # Analytics engine
│   ├── visualization.py          # Charting
│   ├── utils.py                  # Utilities
│   ├── main.py                   # Entry point
│   ├── data/                     # Data files
│   │   ├── trips.csv            # Raw trips
│   │   ├── stations.csv         # Raw stations
│   │   ├── maintenance.csv      # Raw maintenance
│   │   └── *_clean.csv          # Cleaned data (generated)
│   └── tests/                    # Test files
│       └── __init__.py
│
├── output/                        # Generated outputs
│   ├── figures/                  # PNG charts
│   ├── summary_report.txt        # Analytics report
│   └── *.csv                     # Export files
│
├── .github/                       # GitHub configuration
│   ├── workflows/                # CI/CD pipelines
│   └── ISSUE_TEMPLATE/           # Issue templates
│
├── README.md                      # Project documentation
├── CONTRIBUTING.md               # Contribution guidelines
├── CHANGELOG.md                  # Version history
├── DEVELOPMENT.md                # This file
├── SECURITY.md                   # Security policy
├── LICENSE                       # MIT License
├── requirements.txt              # Dependencies
├── .gitignore                    # Git ignore rules
├── .editorconfig                 # Editor settings
├── .pre-commit-config.yaml       # Pre-commit hooks
└── setup_citybike.py            # Setup script
```

### Module Responsibilities

| Module | Purpose | Key Classes |
|--------|---------|-------------|
| models.py | Domain entities | Entity, Bike, Station, User, Trip |
| factories.py | Object creation | Factory functions, DataCache |
| pricing.py | Pricing algorithms | PricingStrategy, TripFareCalculator |
| algorithms.py | Sorting/searching | merge_sort, binary_search, Benchmarks |
| numerical.py | NumPy operations | DistanceCalculator, StatisticalAnalyzer |
| analyzer.py | Data analysis | BikeShareSystem, DataCleaner, Analytics |
| visualization.py | Charting | ChartExporter, TripsAnalyticsCharts |
| utils.py | Helpers | Validators, formatters, utilities |
| main.py | Orchestration | Complete pipeline execution |

## Code Quality Tools

### Black (Code Formatter)

Automatically format code to PEP 8 standards:

```bash
# Format a file
black citybike/models.py

# Format entire package
black citybike/

# Check without modifying
black --check citybike/
```

### Pylint (Linter)

Check code for errors and style issues:

```bash
# Lint a module
pylint citybike/models.py

# Lint entire package
pylint citybike/

# Generate report
pylint citybike/ > pylint_report.txt
```

### MyPy (Type Checker)

Verify type hints correctness:

```bash
# Check a file
mypy citybike/models.py --strict

# Check entire package
mypy citybike/ --ignore-missing-imports

# Strict checking
mypy citybike/ --strict
```

### Flake8 (Style Guide Enforcement)

Check PEP 8 compliance:

```bash
# Install if needed
pip install flake8

# Check code
flake8 citybike/

# With config
flake8 citybike/ --max-line-length=88
```

### Pre-commit Hooks

Run all checks automatically before commit:

```bash
# Install hooks
pre-commit install

# Run manually on all files
pre-commit run --all-files

# Run on specific file
pre-commit run --files citybike/models.py

# Update hook versions
pre-commit autoupdate
```

## Running Tests

### Basic Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest citybike/tests/test_models.py

# Run specific test
pytest citybike/tests/test_models.py::test_bike_creation

# Run with verbose output
pytest -v

# Run with output showing
pytest -s
```

### Test Coverage

```bash
# Run with coverage report
pytest --cov=citybike

# Generate HTML coverage report
pytest --cov=citybike --cov-report=html

# View report
open htmlcov/index.html  # macOS
start htmlcov\index.html  # Windows
```

### Test Markers

```bash
# Run only fast tests
pytest -m fast

# Run only slow tests
pytest -m slow

# Skip specific tests
pytest -m "not integration"
```

### Debugging Tests

```bash
# Stop at first failure
pytest -x

# Drop into debugger on failure
pytest --pdb

# Show local variables on failure
pytest -l
```

## Common Tasks

### Adding a New Module

1. **Create file:** `citybike/new_module.py`
2. **Add docstring:**
   ```python
   """
   Module description.
   
   This module handles...
   """
   ```
3. **Add to `citybike/__init__.py`:**
   ```python
   __all__ = [..., "new_module"]
   ```
4. **Write tests:** `citybike/tests/test_new_module.py`
5. **Update documentation:** `CHANGELOG.md`, `README.md`

### Adding a New Feature

1. **Create feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes:**
   - Write code with type hints
   - Add docstrings (Google style)
   - Add tests
   - Update CHANGELOG.md

3. **Run quality checks:**
   ```bash
   black citybike/
   pylint citybike/
   mypy citybike/
   pytest
   ```

4. **Commit changes:**
   ```bash
   git add .
   git commit -m "feat: add feature description"
   ```

5. **Push and create PR:**
   ```bash
   git push origin feature/your-feature-name
   # Create PR on GitHub
   ```

### Updating Dependencies

```bash
# Check installed versions
pip list

# Check for outdated packages
pip list --outdated

# Update a specific package
pip install --upgrade pandas

# Update all packages
pip install --upgrade -r requirements.txt

# Check for security vulnerabilities
pip-audit

# Generate updated requirements
pip freeze > requirements.txt
```

### Generating Documentation

```bash
# HTML documentation (if Sphinx is setup)
cd docs/
make html

# API documentation from docstrings
pydoc citybike.models
```

### Running the Pipeline

```bash
# Run main pipeline
python -m citybike.main

# With specific data directory
python -c "from citybike.analyzer import BikeShareSystem; \
    system = BikeShareSystem('citybike/data'); \
    system.load_data(); \
    print(system.get_all_analytics())"

# Run specific analysis
python -c "from citybike.analyzer import BikeShareSystem; \
    system = BikeShareSystem('citybike/data'); \
    system.load_data(); \
    print(system.q1_trip_summary())"
```

## Troubleshooting

### Common Issues

#### 1. "ModuleNotFoundError: No module named 'citybike'"

**Solution:**
```bash
# Ensure you're in project root
cd citybike-capstone

# Use -m flag to run as module
python -m citybike.main

# OR add project to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python citybike/main.py
```

#### 2. "ImportError: No module named 'pandas'"

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
python -c "import pandas; print(pandas.__version__)"
```

#### 3. Virtual Environment Not Activating

**Windows PowerShell:**
```powershell
# Allow script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Activate
.venv\Scripts\Activate.ps1
```

#### 4. Pytest Not Finding Tests

**Solution:**
```bash
# Ensure tests have __init__.py
touch citybike/tests/__init__.py

# Run with explicit path
pytest citybike/tests/

# Check test discovery
pytest --collect-only
```

#### 5. Pre-commit Hook Failures

**Solution:**
```bash
# Uninstall hooks temporarily
pre-commit uninstall

# Fix issues manually
black citybike/
pylint citybike/

# Reinstall hooks
pre-commit install
```

### Getting Help

1. **Check documentation:**
   - README.md - Project overview
   - CONTRIBUTING.md - Guidelines
   - Docstrings - Code documentation

2. **Search issues:**
   - GitHub Issues - Known problems
   - GitHub Discussions - Q&A

3. **Ask for help:**
   - Email: mutabazi105@gmail.com
   - GitHub Issues (mark as question)

## Development Tips

### Best Practices

✅ **DO:**
- Write type hints for all functions
- Add comprehensive docstrings
- Write tests for new features
- Use meaningful commit messages
- Keep commits focused and small
- Update documentation with code changes

❌ **DON'T:**
- Commit development tools or venv
- Use magic numbers (use constants)
- Write overly complex functions
- Ignore type checking errors
- Forget to handle exceptions
- Commit sensitive information

### Code Style

```python
# Good: Type hints and docstrings
def calculate_fare(distance: float, duration: int) -> float:
    """
    Calculate trip fare.
    
    Args:
        distance: Trip distance in km
        duration: Trip duration in minutes
    
    Returns:
        Fare in euros
        
    Raises:
        ValueError: If inputs are negative
    """
    if distance < 0 or duration < 0:
        raise ValueError("Distance and duration must be positive")
    return distance * 0.80 + duration * 0.30

# Good: Clear naming and organization
class BikeShareSystem:
    """Orchestrator for bike-sharing analytics."""
    
    def __init__(self, data_dir: str):
        """Initialize system."""
        self.data_dir = data_dir
```

### Performance Tips

- Use NumPy for numerical operations (vectorized)
- Use Pandas for data manipulation
- Avoid nested loops where possible
- Profile code with `cProfile` before optimizing
- Use generators for large datasets

### Documentation Tips

- Keep docstrings concise but complete
- Use Google style format
- Include type hints in docstrings
- Provide examples where useful
- Update CHANGELOG.md with changes

---

**Last Updated:** 2026-02-09

For more information, see:
- [README.md](README.md) - Project overview
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [CHANGELOG.md](CHANGELOG.md) - Version history
- [SECURITY.md](SECURITY.md) - Security policy
