"""
CityBike Analytics Platform - Package Initialization

A comprehensive bike-sharing analytics platform demonstrating professional Python
software engineering practices including OOP design patterns, algorithm implementations,
and data analysis pipelines.

Modules:
    - models: Domain-driven design with entity hierarchy
    - factories: Factory Pattern for object creation
    - pricing: Strategy Pattern for dynamic pricing algorithms
    - algorithms: Custom sorting/searching with complexity analysis
    - numerical: NumPy-based numerical computations
    - analyzer: Data cleaning and 14 business analytics queries
    - visualization: Matplotlib-based professional charting
    - utils: Validation helpers and formatting utilities
    - main: Complete pipeline orchestration

Design Patterns Used:
    - Factory Pattern: Dynamic object creation without exposing subclasses
    - Strategy Pattern: Interchangeable pricing algorithms
    - Abstract Base Classes: Entity hierarchy and interface contracts
    - Data Cleaner Pattern: CSV data validation and transformation

Example:
    >>> from citybike.analyzer import BikeShareSystem
    >>> system = BikeShareSystem(data_dir="citybike/data")
    >>> system.load_data()
    >>> analytics = system.get_all_analytics()

Version: 1.0.0
Author: Bernard TURIKUMANA
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Bernard TURIKUMANA"
__all__ = [
    "models",
    "factories",
    "pricing",
    "algorithms",
    "numerical",
    "analyzer",
    "visualization",
    "utils",
]
