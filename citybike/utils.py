"""
Utility functions for validation, formatting, and data processing.
Helpers for input validation, date parsing, and formatting.
"""
import re
from datetime import datetime
from typing import Any, Optional


# Regex patterns
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
DATE_REGEX = r'^\d{4}-\d{2}-\d{2}$'
TIME_REGEX = r'^\d{2}:\d{2}:\d{2}$'
DATETIME_REGEX = r'^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}$'


def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email string to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not email or not isinstance(email, str):
        return False
    return bool(re.match(EMAIL_REGEX, email))


def validate_date(date_string: str) -> bool:
    """
    Validate date format (YYYY-MM-DD).
    
    Args:
        date_string: Date string to validate
        
    Returns:
        True if valid format, False otherwise
    """
    if not date_string or not isinstance(date_string, str):
        return False
    return bool(re.match(DATE_REGEX, date_string))


def validate_datetime(datetime_string: str) -> bool:
    """
    Validate datetime format (YYYY-MM-DD HH:MM:SS).
    
    Args:
        datetime_string: Datetime string to validate
        
    Returns:
        True if valid format, False otherwise
    """
    if not datetime_string or not isinstance(datetime_string, str):
        return False
    return bool(re.match(DATETIME_REGEX, datetime_string))


def parse_datetime(date_string: str) -> Optional[datetime]:
    """
    Parse datetime string to datetime object.
    
    Args:
        date_string: String in format 'YYYY-MM-DD HH:MM:SS'
        
    Returns:
        datetime object or None if parsing fails
    """
    try:
        return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        return None


def parse_date(date_string: str) -> Optional[datetime]:
    """
    Parse date string to datetime object.
    
    Args:
        date_string: String in format 'YYYY-MM-DD'
        
    Returns:
        datetime object or None if parsing fails
    """
    try:
        return datetime.strptime(date_string, "%Y-%m-%d")
    except (ValueError, TypeError):
        return None


def format_currency(amount: float, currency: str = "€") -> str:
    """
    Format currency value.
    
    Args:
        amount: Numeric amount
        currency: Currency symbol
        
    Returns:
        Formatted currency string
    """
    return f"{currency}{amount:.2f}"


def format_distance(distance_km: float, unit: str = "km") -> str:
    """
    Format distance value.
    
    Args:
        distance_km: Distance in kilometers
        unit: Unit of measurement
        
    Returns:
        Formatted distance string
    """
    return f"{distance_km:.2f} {unit}"


def format_duration(minutes: float) -> str:
    """
    Format trip duration to readable string.
    
    Args:
        minutes: Duration in minutes
        
    Returns:
        Formatted duration (e.g., "1h 30m")
    """
    total_minutes = int(minutes)
    hours = total_minutes // 60
    mins = total_minutes % 60
    
    if hours > 0:
        return f"{hours}h {mins}m"
    return f"{mins}m"


def format_percentage(value: float, total: float) -> str:
    """
    Format as percentage.
    
    Args:
        value: Numerator
        total: Denominator
        
    Returns:
        Percentage string (e.g., "45.5%")
    """
    if total == 0:
        return "0.0%"
    return f"{(value / total) * 100:.1f}%"


def validate_coordinate(value: float, coord_type: str = "latitude") -> bool:
    """
    Validate geographic coordinate.
    
    Args:
        value: Coordinate value
        coord_type: "latitude" or "longitude"
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(value, (int, float)):
        return False
    
    if coord_type.lower() == "latitude":
        return -90 <= value <= 90
    elif coord_type.lower() == "longitude":
        return -180 <= value <= 180
    
    return False


def calculate_distance_euclidean(
    lat1: float, lon1: float,
    lat2: float, lon2: float
) -> float:
    """
    Calculate simple Euclidean distance between two coordinates.
    (Simplified flat-earth model, not for real GPS routing)
    
    Args:
        lat1, lon1: First coordinate
        lat2, lon2: Second coordinate
        
    Returns:
        Distance in degrees (scale factor varies by latitude)
    """
    import math
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    return math.sqrt(dlat**2 + dlon**2)


def clamp_value(value: float, min_val: float, max_val: float) -> float:
    """
    Clamp value to range [min_val, max_val].
    
    Args:
        value: Value to clamp
        min_val: Minimum value
        max_val: Maximum value
        
    Returns:
        Clamped value
    """
    return max(min_val, min(value, max_val))


class ValidationError(ValueError):
    """Custom exception for validation failures."""
    pass


class DataCleaningStrategy:
    """Strategy for handling missing data."""
    
    STRATEGIES = {
        "drop": "Remove rows with missing values",
        "fill_zero": "Fill with 0",
        "fill_mean": "Fill with mean value",
        "fill_forward": "Forward fill (for time series)",
        "fill_back": "Backward fill (for time series)",
    }
    
    @staticmethod
    def describe() -> dict:
        """Return available strategies."""
        return DataCleaningStrategy.STRATEGIES.copy()
