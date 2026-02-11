# CityBike Analytics Platform

A Python project for analyzing bike-sharing operations.

## Features

- **Object-Oriented Programming** - Bikes, Stations, Users, and Trips classes
- **Data Processing** - Loads and cleans CSV files
- **Analytics** - Answers 14 business questions about bike usage
- **Algorithms** - Sorting (merge sort, quick sort) and searching (binary search)
- **NumPy** - Statistical analysis and calculations
- **Visualizations** - 10+ Matplotlib charts

## ✅ Project Milestones

| # | Milestone | Status |
|---|-----------|--------|
| 1 | Project Structure & Setup | ✅ Complete |
| 2 | Domain Models (OOP) | ✅ Complete |
| 3 | Data Loading & Cleaning | ✅ Complete |
| 4 | Custom Algorithms | ✅ Complete |
| 5 | NumPy Numerical Analysis | ✅ Complete |
| 6 | 14 Business Analytics Queries | ✅ Complete |
| 7 | Matplotlib Visualizations | ✅ Complete |
| 8 | Testing & Documentation | ✅ Complete |
| 9 | Presentation Ready | ✅ Complete |

## Installation

```bash
pip install -r requirements.txt
```

## How to Run

```bash
python -m citybike.main
```

This will:
- Load data from `citybike/data/`
- Clean and validate the data
- Generate 14 analytics reports
- Create visualizations in `output/figures/`
- Export summaries to `output/`

## Project Structure

```
citybike/
├── main.py           # Run the pipeline
├── models.py         # Classes for Bike, Station, User, Trip
├── factories.py      # Factory Pattern
├── analyzer.py       # Analytics engine
├── algorithms.py     # Sorting and searching
├── numerical.py      # NumPy calculations
├── pricing.py        # Pricing strategies
├── visualization.py  # Charts and graphs
└── utils.py          # Helper functions
```

## Data

- `citybike/data/trips.csv` - Trip records
- `citybike/data/stations.csv` - Station information
- `citybike/data/maintenance.csv` - Maintenance records

## Output

- `output/figures/` - Charts (PNG files)
- `output/summary_report.txt` - Text report
- `output/top_users.csv` - Most active users
- `output/top_routes.csv` - Most popular routes

## Requirements

- Python 3.8+
- pandas
- numpy
- matplotlib
- python-dateutil

## 👨‍💻 Author

**Bernard Turikumana**  
[GitHub](https://github.com/mutabazi105) | [Project Repository](https://github.com/mutabazi105/citybike-capstone)

## 📄 Project Requirements

See [`Project_Requirements.pdf`](./Project_Requirements.pdf) for complete business and technical specifications.

## License

MIT
