# 🚴 CityBike: Bike-Sharing Analytics Platform

A comprehensive Python backend platform for analyzing bike-sharing operations. This capstone project demonstrates mastery of object-oriented design, data analysis, algorithms, and professional software engineering practices.

## 📋 Project Overview

**CityBike** is a complete analytics system for a fictional bike-sharing service. It loads operational datasets, cleans and validates data, implements custom algorithms, performs statistical analysis, and generates professional visualizations.

### Key Features

✅ **Object-Oriented Design**
- Abstract base classes and inheritance hierarchies
- Factory Pattern for object creation
- Strategy Pattern for dynamic pricing models
- Full input validation and error handling

✅ **Data Processing**
- Loads and cleans 3 CSV datasets (1500+ raw records)
- Handles missing values with documented strategies
- Type conversion and duplicate removal
- Data quality validation

✅ **Advanced Algorithms**
- Custom merge sort & quick sort implementation (O(n log n))
- Binary search algorithms (O(log n))
- Complexity analysis with benchmarking
- Performance comparison vs Python built-ins

✅ **Numerical Computing**
- NumPy-based statistical analysis
- Euclidean distance calculations
- Outlier detection (Z-score and IQR methods)
- Vectorized batch computations

✅ **Business Analytics**
- 14 key business questions answered
- Pandas aggregations and groupby operations
- Monthly trends, user segmentation, utilization rates
- Maintenance cost analysis

✅ **Professional Visualizations**
- 10+ Matplotlib charts
- Bar charts, line plots, histograms, box plots, pie charts
- Proper labels, legends, and styling
- PNG export for presentations

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone <your-repo-url>
cd citybike-capstone

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run Analytics Pipeline

```bash
python citybike/main.py
```

**Generates:**
- ✅ Cleaned CSV datasets in `citybike/data/`
- ✅ Summary report in `output/summary_report.txt`
- ✅ 10+ PNG charts in `output/figures/`
- ✅ Analysis results in `output/*.csv`

## 📊 14 Business Questions Answered

1. **Total trips, distance, average duration**
2. **Top 10 most popular stations (start & end)**
3. **Peak usage hours during the day**
4. **Day of week with highest trip volume**
5. **Average trip distance by user type**
6. **Bike utilization rate (%)**
7. **Monthly ridership trend (growth analysis)**
8. **Top 15 most active users**
9. **Total maintenance cost per bike type**
10. **Top 10 origin-destination routes**
11. **Trip completion rate (vs cancelled)**
12. **Average trips per user by type**
13. **Bikes with highest maintenance frequency**
14. **Outlier detection (unusual trips)**

## 🏗️ Project Architecture

### Module Responsibilities

| Module | Purpose | Lines |
|--------|---------|-------|
| `models.py` | OOP domain classes with validation | 664 |
| `factories.py` | Factory Pattern object creation | 207 |
| `analyzer.py` | BikeShareSystem: data analysis hub | 584 |
| `algorithms.py` | Sorting/searching with complexity | 416 |
| `numerical.py` | NumPy: statistics, distances, outliers | 350 |
| `pricing.py` | Strategy Pattern: dynamic pricing | 296 |
| `visualization.py` | Matplotlib professional charts | 489 |
| `utils.py` | Validation, formatting, helpers | 234 |
| `main.py` | Orchestration: complete pipeline | 269 |

**Total:** ~3,500 lines of production-quality Python code

### Design Patterns Implemented

#### Factory Pattern (`factories.py`)
Create domain objects without exposing subclass constructors:
```python
bike = create_bike("BK001", "electric", "available")
user = create_user("USR001", "casual")
trip = create_trip(row_dict, users_cache, bikes_cache, stations_cache)
```

#### Strategy Pattern (`pricing.py`)
Interchangeable pricing strategies:
- **CasualPricing** - €0.30/min (for pay-per-ride users)
- **MemberPricing** - €0.18/min with 45-minute free rides
- **PeakHourPricing** - +50% surcharge during rush hours (8-9am, 5-7pm)
- **DistanceBasedPricing** - €0.80/km alternative

```python
calculator = TripFareCalculator(MemberPricingStrategy())
fare = calculator.calculate(duration=45, distance=5.2, bike_type="classic")
```

### Algorithms Implemented

#### Sorting Algorithms
- **Merge Sort** → O(n log n) stable, consistent
- **Quick Sort** → O(n log n) average, fast in practice
- **Bubble Sort** → O(n²) for comparison/learning

#### Searching Algorithms
- **Binary Search** → O(log n) iterative
- **Binary Search** → O(log n) recursive
- **Linear Search** → O(n) for unsorted data

**Benchmarked against:** Python's `sorted()` and `.index()` methods

## 🧪 Data Cleaning Pipeline

**Input:** 3 raw CSV files with intentional data quality issues
- Missing values in duration, distance, cost
- Invalid timestamps (end_time before start_time)
- Duplicate records
- Type inconsistencies

**Cleaning Steps:**
1. Parse datetime strings with validation
2. Convert to proper numeric types
3. Remove rows with invalid times
4. Fill missing distances with mean value
5. Remove duplicate records by ID
6. Validate coordinates (±90° lat, ±180° lon)
7. Validate capacity (> 0)

**Output:** 3 validated CSV files ready for analysis

## 📊 Visualizations (10+ Charts)

1. **Top Stations** - Bar chart of most popular start/end stations
2. **Monthly Trend** - Line chart showing ridership growth over time
3. **Duration Distribution** - Histogram with mean/median lines
4. **Distance Distribution** - Histogram of trip distances
5. **User Type Comparison** - Box plot: Casual vs Member duration
6. **Bike Type Comparison** - Box plot: Classic vs Electric duration
7. **Trip Status** - Pie chart: Completed vs Cancelled rates
8. **Maintenance Cost** - Bar chart: Cost breakdown by bike type
9. **Maintenance Types** - Bar chart: Repair frequency by type
10. **Hourly Usage** - Line chart: Peak hours highlighted in red

All exported as high-resolution PNG to `output/figures/`

## 🧮 NumPy Integration

### Statistical Analysis
```python
from citybike.numerical import StatisticalAnalyzer

stats = StatisticalAnalyzer.compute_statistics(durations)
# Returns: count, mean, median, std, min, max, q25, q75, q90
```

### Distance Calculations
```python
from citybike.numerical import DistanceCalculator

# Single distance
dist = DistanceCalculator.euclidean_distance(48.8, 9.16, 48.8, 9.20)

# Vectorized pairwise distances for all stations
distances = DistanceCalculator.pairwise_distances(station_coords)
```

### Outlier Detection
```python
from citybike.numerical import OutlierDetection

# Z-score method
outliers, z_scores = OutlierDetection.zscore_outliers(data, threshold=3.0)

# IQR method  
outliers, bounds = OutlierDetection.iqr_outliers(data, iqr_multiplier=1.5)

# Isolation Forest scores
scores = OutlierDetection.isolation_forest_scores(data)
```

## 🎯 Milestones Completed

- ✅ **Milestone 1** - Project setup with structure, requirements, data
- ✅ **Milestone 2** - OOP domain models with inheritance, validation
- ✅ **Milestone 3** - Data loading, cleaning, export
- ✅ **Milestone 4** - Custom sorting/searching algorithms with Big-O
- ✅ **Milestone 5** - NumPy statistical computing
- ✅ **Milestone 6** - 14 business analytics queries
- ✅ **Milestone 7** - 10+ professional Matplotlib visualizations
- ✅ **Milestone 8** - Documentation and final polish

## 📁 Complete Project Structure

```
citybike-capstone/
├── citybike/
│   ├── __init__.py
│   ├── main.py                 # Entry point & orchestration
│   ├── models.py              # OOP domain classes (664 lines)
│   ├── factories.py           # Factory Pattern (207 lines)
│   ├── analyzer.py            # BikeShareSystem & analytics (584 lines)
│   ├── algorithms.py          # Sorting, searching (416 lines)
│   ├── numerical.py           # NumPy operations (350 lines)
│   ├── pricing.py             # Strategy Pattern (296 lines)
│   ├── visualization.py       # Matplotlib charts (489 lines)
│   ├── utils.py               # Helpers & validation (234 lines)
│   ├── data/
│   │   ├── trips.csv
│   │   ├── stations.csv
│   │   ├── maintenance.csv
│   │   ├── trips_clean.csv         (generated)
│   │   ├── stations_clean.csv      (generated)
│   │   └── maintenance_clean.csv   (generated)
│   ├── output/
│   │   ├── summary_report.txt
│   │   ├── top_users.csv
│   │   ├── top_routes.csv
│   │   └── figures/
│   │       ├── 01_top_stations.png
│   │       ├── 02_monthly_trend.png
│   │       ├── 03_duration_distribution.png
│   │       └── ... (10+ charts)
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   └── test_algorithms.py
│   └── __pycache__/
├── citybike/
├── data_generator.py
├── setup_citybike.py
├── requirements.txt
├── README.md              (this file)
└── .gitignore
```

## 📋 Dependencies

```
pandas>=1.5.0          # Data analysis & aggregation
numpy>=1.24.0          # Numerical computing
matplotlib>=3.7.0      # Chart generation
python-dateutil>=2.8.0 # Date/time parsing
pytest>=7.0.0          # Testing (optional)
```

## ✨ Code Quality Standards

- ✅ **Type Hints** - All functions annotated (PEP 484)
- ✅ **Docstrings** - Every module, class, and function documented
- ✅ **PEP 8** - Code style follows Python conventions
- ✅ **DRY Principle** - No code duplication
- ✅ **Separation of Concerns** - Business logic isolated from I/O
- ✅ **Error Handling** - Comprehensive validation
- ✅ **Named Constants** - No magic numbers

## 🔗 Git & Version Control

**Branch Strategy:**
- `feature/oop-models` - Development branch (current)
- `main` - Production branch (ready for merge)

**Commit History:** (9 meaningful commits)
```
✓ feat: implement main orchestration pipeline
✓ feat: implement visualization module (10+ charts)
✓ feat: implement analyzer (14 analytics queries)
✓ feat: implement numerical module (NumPy)
✓ feat: implement algorithms (sorting/searching)
✓ feat: implement pricing (Strategy Pattern)
✓ feat: implement utils (helpers & validation)
✓ feat: implement factories (Factory Pattern)
✓ refactor: Entity inheritance for Trip/MaintenanceRecord
```

All commits follow conventional commit style for clarity and professionalism.

## 🧪 Testing (Optional)

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_models.py -v

# Run with coverage report
pytest tests/ --cov=citybike
```

## 🎓 What This Project Demonstrates

✅ **Object-Oriented Programming** - Inheritance, polymorphism, encapsulation  
✅ **Design Patterns** - Factory, Strategy in real-world applications  
✅ **Algorithms** - Custom implementations with Big-O analysis  
✅ **Data Science** - Pandas/NumPy for analysis at scale  
✅ **Professional Practices** - Git, documentation, testing, code quality  
✅ **Problem Solving** - Real-world data cleaning and analysis challenges  

## 📞 Usage Examples

### Load and Analyze Data
```python
from citybike.analyzer import BikeShareSystem

system = BikeShareSystem(data_dir="citybike/data")
system.load_data()
system.clean_data()
system.export_cleaned_data()

# Get all analytics
analytics = system.get_all_analytics()
print(analytics["Q1_summary"])  # Trip summary
print(analytics["Q2_popular_stations"])  # Top stations
```

### Use Pricing Strategies
```python
from citybike.pricing import PricingFactory, TripFareCalculator

# Create Member pricing strategy
strategy = PricingFactory.create_strategy("member")
calculator = TripFareCalculator(strategy)

# Calculate fare
result = calculator.calculate(duration_minutes=50, distance_km=12.5)
print(f"Fare: {result['fare']}€")
```

### Benchmark Algorithms
```python
from citybike.algorithms import SortingBenchmark, ComplexityAnalysis

# Compare sorting algorithms
data = list(range(1000))
times = SortingBenchmark.compare_algorithms(data)

# Get complexity analysis
analysis = ComplexityAnalysis.get_analysis("merge_sort")
print(ComplexityAnalysis.print_report())
```

## 🏁 Status

**✅ PROJECT COMPLETE AND PRODUCTION-READY**

All requirements from capstone specification implemented:
- ✅ 8 modules with clear responsibilities
- ✅ OOP with inheritance and properties
- ✅ Both design patterns (Factory, Strategy)
- ✅ Custom algorithms with benchmarking
- ✅ NumPy vectorized operations
- ✅ 14 business questions answered
- ✅ 10+ professional visualizations
- ✅ Clean code with documentation
- ✅ Git version control
- ✅ Professional README

---

**Last Updated:** February 9, 2026  
**Python Version:** 3.8+  
**License:** MIT  
**Status:** Ready for deployment 🚀
