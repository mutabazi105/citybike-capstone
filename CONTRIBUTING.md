# Contributing to CityBike Analytics Platform

Thank you for your interest in contributing to the CityBike Analytics Platform! This document provides guidelines and instructions for contributing to the project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing](#testing)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

Be respectful, inclusive, and constructive in all interactions with the community.

## Getting Started

### 1. Fork & Clone Repository

```bash
git clone https://github.com/<your-username>/citybike-capstone.git
cd citybike-capstone
```

### 2. Setup Development Environment

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows PowerShell
source .venv/bin/activate  # Mac/Linux

# Install dependencies with dev packages
pip install -r requirements.txt
pip install black pylint mypy pytest
```

### 3. Verify Installation

```bash
python -m citybike.main
```

## Development Workflow

### 1. Create Feature Branch

```bash
# Create branch from main
git checkout main
git pull origin main
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Follow code style guidelines (see below)
- Add docstrings to all functions
- Include type hints
- Write tests for new features

### 3. Format & Lint Code

```bash
# Auto-format with Black
black citybike/

# Check with Pylint
pylint citybike/

# Type checking
mypy citybike/
```

## Code Style Guidelines

### Python Standards (PEP 8)

- **Line length:** 88 characters (Black default)
- **Indentation:** 4 spaces (no tabs)
- **Naming:**
  - Classes: `PascalCase` (e.g., `BikeShareSystem`)
  - Functions/Variables: `snake_case` (e.g., `calculate_fare()`)
  - Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_BIKE_AGE`)

### Docstring Format (Google Style)

```python
def calculate_fare(distance: float, duration: int) -> float:
    """
    Calculate trip fare based on distance and duration.

    Args:
        distance: Trip distance in kilometers
        duration: Trip duration in minutes

    Returns:
        Calculated fare in euros

    Raises:
        ValueError: If distance or duration is negative
    
    Example:
        >>> calculate_fare(5.0, 30)
        8.5
    """
    # Implementation
    pass
```

### Type Hints

```python
# Good
def load_data(path: str) -> pd.DataFrame:
    """Load CSV data from file."""
    pass

# Avoid
def load_data(path):
    """Load CSV data from file."""
    pass
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest citybike/tests/test_models.py

# Run with coverage
pytest --cov=citybike
```

### Writing Tests

```python
# tests/test_models.py
import pytest
from citybike.models import Bike, ClassicBike

def test_bike_creation():
    """Test bike instantiation."""
    bike = ClassicBike(bike_id="BK001", gear_count=21)
    assert bike.id == "BK001"
    assert bike.gear_count == 21

def test_invalid_bike():
    """Test bike validation."""
    with pytest.raises(ValueError):
        ClassicBike(bike_id="", gear_count=21)
```

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat:** New feature
- **fix:** Bug fix
- **docs:** Documentation changes
- **refactor:** Code refactoring without feature changes
- **test:** Adding/updating tests
- **perf:** Performance improvements
- **style:** Code formatting (Black, linting)
- **chore:** Dependencies, tools, etc.

### Examples

```bash
# Good
git commit -m "feat(pricing): add peak-hour pricing strategy"
git commit -m "fix(analyzer): handle missing maintenance records"
git commit -m "docs(readme): update setup instructions"

# Avoid
git commit -m "fixed stuff"
git commit -m "updated code"
```

## Pull Request Process

### Before Submitting

1. **Update main:** `git pull origin main`
2. **Rebase branch:** `git rebase main feature/your-feature`
3. **Test locally:** `python -m citybike.main`
4. **Check linting:** `pylint citybike/`
5. **Run tests:** `pytest`

### Submitting PR

1. Push branch: `git push origin feature/your-feature`
2. Open Pull Request on GitHub
3. Fill out PR template:
   - **Description:** What changes? Why?
   - **Type:** Bug fix / Feature / Refactor
   - **Testing:** How was it tested?
   - **Breaking changes:** Any backward incompatibility?

### PR Requirements

- ✅ Passes all tests
- ✅ Code meets style guidelines
- ✅ Documentation updated
- ✅ No merge conflicts
- ✅ Meaningful commit messages

### Review & Merge

- Project maintainers will review
- Request changes if needed
- Once approved, maintainer will merge

## Project Structure Best Practices

```
citybike-capstone/
├── citybike/              # Main package
│   ├── __init__.py       # Package initialization
│   ├── models.py         # Domain models
│   ├── factories.py      # Factory Pattern
│   ├── analyzer.py       # Analytics engine
│   ├── data/             # Raw data files
│   └── tests/            # Unit tests
├── output/               # Generated outputs
├── README.md            # Project documentation
├── requirements.txt     # Dependencies
├── LICENSE              # MIT License
└── setup_citybike.py   # Setup script
```

## Resources

- [Python Style Guide (PEP 8)](https://pep8.org/)
- [NumPy Documentation](https://numpy.org/doc/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [Matplotlib Documentation](https://matplotlib.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)

## Questions?

- Open an Issue on GitHub
- Check existing Issues/Discussions
- Review Project Documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Happy Contributing!** 🚀

