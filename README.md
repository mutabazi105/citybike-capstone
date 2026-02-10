# CityBike Analytics Platform

A Python project for analyzing bike-sharing operations.

## Features

- **Object-Oriented Programming** - Bikes, Stations, Users, and Trips classes
- **Data Processing** - Loads and cleans CSV files
- **Analytics** - Answers 14 business questions about bike usage
- **Algorithms** - Sorting (merge sort, quick sort) and searching (binary search)
- **NumPy** - Statistical analysis and calculations
- **Visualizations** - 10+ Matplotlib charts

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

## License

MIT
