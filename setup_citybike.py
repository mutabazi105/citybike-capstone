# setup_citybike.py
import os
import sys


def create_structure():
    """Create the complete CityBike project structure."""
    print("🚲 Creating CityBike Project Structure...")
    print("=" * 50)

    # Create directories
    directories = [
        "citybike/data",
        "citybike/output/figures",
        "citybike/tests",
        "output/figures"
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Created: {directory}/")

    # Create Python files
    python_files = [
        "citybike/__init__.py",
        "citybike/main.py",
        "citybike/models.py",
        "citybike/analyzer.py",
        "citybike/algorithms.py",
        "citybike/numerical.py",
        "citybike/visualization.py",
        "citybike/pricing.py",
        "citybike/factories.py",
        "citybike/utils.py",
        "citybike/tests/__init__.py",
        "citybike/tests/test_models.py",
        "citybike/tests/test_algorithms.py"
    ]

    for file_path in python_files:
        with open(file_path, 'w') as f:
            f.write("")
        print(f"📄 Created: {file_path}")

    # Create configuration files with content
    config_files = {
        "requirements.txt": """pandas>=1.5.0
numpy>=1.24.0
matplotlib>=3.7.0
python-dateutil>=2.8.0
pytest>=7.0.0  # optional""",

        ".gitignore": """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
.venv
venv/
ENV/
env/
env.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Project specific
output/figures/*.png
citybike/data/*_clean.csv
output/summary_report.txt
"""
    }

    for file_path, content in config_files.items():
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"⚙️  Created: {file_path}")

    print("\n" + "=" * 50)
    print("✅ Project structure created successfully!")
    print("\nNext steps:")
    print("1. Install packages: pip install -r requirements.txt")
    print("2. Create data_generator.py")
    print("3. Start coding in citybike/models.py")


if __name__ == "__main__":
    create_structure()
