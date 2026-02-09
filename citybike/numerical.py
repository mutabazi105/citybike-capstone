"""
Numerical computing module using NumPy.
Handles distance calculations, statistics, and outlier detection.
"""
import numpy as np
from typing import Tuple, List, Optional, Dict
import math


class DistanceCalculator:
    """Calculate distances between geographic coordinates."""

    @staticmethod
    def euclidean_distance(lat1: float, lon1: float,
                          lat2: float, lon2: float) -> float:
        """
        Calculate Euclidean distance between two points (simplified flat-earth).
        
        Formula: d = sqrt((lat2-lat1)² + (lon2-lon1)²)
        
        Args:
            lat1, lon1: First coordinate
            lat2, lon2: Second coordinate
            
        Returns:
            Distance in degrees (not adjusted for latitude)
        """
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        return math.sqrt(dlat**2 + dlon**2)

    @staticmethod
    def pairwise_distances(stations_coords: np.ndarray) -> np.ndarray:
        """
        Calculate pairwise distances between all stations.
        
        Args:
            stations_coords: Array of shape (n_stations, 2) with [lat, lon]
            
        Returns:
            Distance matrix of shape (n_stations, n_stations)
        """
        # Extract coordinates
        coords = np.array(stations_coords)
        n = len(coords)

        # Create distance matrix
        distances = np.zeros((n, n))

        for i in range(n):
            for j in range(i + 1, n):
                lat1, lon1 = coords[i]
                lat2, lon2 = coords[j]

                dist = DistanceCalculator.euclidean_distance(
                    lat1, lon1, lat2, lon2
                )

                distances[i, j] = dist
                distances[j, i] = dist  # Symmetric

        return distances

    @staticmethod
    def nearest_station(from_station_idx: int,
                       distance_matrix: np.ndarray) -> int:
        """
        Find nearest station to a given station (excluding itself).
        
        Args:
            from_station_idx: Index of reference station
            distance_matrix: Precomputed distance matrix
            
        Returns:
            Index of nearest station
        """
        distances = distance_matrix[from_station_idx].copy()
        distances[from_station_idx] = np.inf  # Exclude self
        return int(np.argmin(distances))


class StatisticalAnalyzer:
    """Compute statistical summaries using NumPy."""

    @staticmethod
    def compute_statistics(data: np.ndarray) -> Dict[str, float]:
        """
        Compute comprehensive statistics on a dataset.
        
        Args:
            data: NumPy array of numeric values
            
        Returns:
            Dictionary with statistical measures
        """
        data = np.asarray(data)
        data = data[~np.isnan(data)]  # Remove NaN values

        if len(data) == 0:
            return {
                "count": 0,
                "mean": np.nan,
                "median": np.nan,
                "std": np.nan,
                "min": np.nan,
                "max": np.nan,
                "q25": np.nan,
                "q75": np.nan,
            }

        return {
            "count": len(data),
            "mean": float(np.mean(data)),
            "median": float(np.median(data)),
            "std": float(np.std(data)),
            "min": float(np.min(data)),
            "max": float(np.max(data)),
            "q25": float(np.percentile(data, 25)),
            "q75": float(np.percentile(data, 75)),
            "q90": float(np.percentile(data, 90)),
        }

    @staticmethod
    def percentile_analysis(data: np.ndarray,
                           percentiles: List[int] = None) -> Dict[int, float]:
        """
        Calculate percentiles for a dataset.
        
        Args:
            data: NumPy array
            percentiles: List of percentile values (0-100)
            
        Returns:
            Dictionary mapping percentile to value
        """
        if percentiles is None:
            percentiles = [10, 25, 50, 75, 90, 95, 99]

        data = np.asarray(data)
        data = data[~np.isnan(data)]

        return {
            p: float(np.percentile(data, p))
            for p in percentiles
        }


class OutlierDetection:
    """Identify and analyze outliers in datasets."""

    @staticmethod
    def zscore_outliers(data: np.ndarray,
                       threshold: float = 3.0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Identify outliers using Z-score method.
        Points with |z-score| > threshold are outliers.
        
        Args:
            data: NumPy array of values
            threshold: Z-score threshold (typically 2.0 or 3.0)
            
        Returns:
            Tuple of (outlier_mask, z_scores)
        """
        data = np.asarray(data, dtype=float)
        mask = ~np.isnan(data)

        clean_data = data[mask]
        mean = np.mean(clean_data)
        std = np.std(clean_data)

        if std == 0:
            return np.zeros_like(data, dtype=bool), np.zeros_like(data)

        z_scores = np.zeros_like(data, dtype=float)
        z_scores[mask] = (clean_data - mean) / std

        outliers = np.abs(z_scores) > threshold

        return outliers, z_scores

    @staticmethod
    def iqr_outliers(data: np.ndarray,
                     iqr_multiplier: float = 1.5) -> Tuple[np.ndarray, Dict]:
        """
        Identify outliers using Interquartile Range (IQR) method.
        
        Args:
            data: NumPy array
            iqr_multiplier: Multiplier for IQR (typically 1.5)
            
        Returns:
            Tuple of (outlier_mask, bounds_dict)
        """
        data = np.asarray(data, dtype=float)
        clean_data = data[~np.isnan(data)]

        q1 = np.percentile(clean_data, 25)
        q3 = np.percentile(clean_data, 75)
        iqr = q3 - q1

        lower_bound = q1 - iqr_multiplier * iqr
        upper_bound = q3 + iqr_multiplier * iqr

        outliers = (data < lower_bound) | (data > upper_bound)

        return outliers, {
            "q1": float(q1),
            "q3": float(q3),
            "iqr": float(iqr),
            "lower_bound": float(lower_bound),
            "upper_bound": float(upper_bound),
        }

    @staticmethod
    def isolation_forest_scores(data: np.ndarray,
                               contamination: float = 0.1) -> np.ndarray:
        """
        Simple outlier scoring (not full isolation forest).
        Higher score = more likely to be outlier.
        
        Args:
            data: 1D or 2D NumPy array
            contamination: Expected proportion of outliers
            
        Returns:
            Anomaly scores (0-1, higher = more anomalous)
        """
        data = np.asarray(data, dtype=float)

        if data.ndim == 1:
            data = data.reshape(-1, 1)

        # Simple approach: distance from mean in normalized space
        mean = np.mean(data, axis=0)
        std = np.std(data, axis=0)
        std[std == 0] = 1  # Avoid division by zero

        normalized = (data - mean) / std
        distances = np.linalg.norm(normalized, axis=1)

        # Normalize to 0-1
        d_min, d_max = np.min(distances), np.max(distances)
        if d_max == d_min:
            scores = np.zeros_like(distances)
        else:
            scores = (distances - d_min) / (d_max - d_min)

        return scores


class BatchNumericalComputation:
    """Vectorized computation over multiple records."""

    @staticmethod
    def calculate_fares(durations: np.ndarray,
                       distances: np.ndarray,
                       rate_per_minute: float = 0.30,
                       rate_per_km: float = 0.80) -> np.ndarray:
        """
        Vectorized fare calculation.
        
        Args:
            durations: Array of trip durations in minutes
            distances: Array of trip distances in km
            rate_per_minute: €/minute
            rate_per_km: €/km
            
        Returns:
            Array of fare amounts
        """
        duration_fare = durations * rate_per_minute
        distance_fare = distances * rate_per_km

        # Use maximum of both calculations
        fares = np.maximum(duration_fare, distance_fare)

        # Apply minimum fare of €2.00
        fares = np.maximum(fares, 2.00)

        return np.round(fares, 2)

    @staticmethod
    def split_by_status(statuses: np.ndarray,
                       data: np.ndarray) -> Dict[str, np.ndarray]:
        """
        Split data by categorical status.
        
        Args:
            statuses: Array of status strings
            data: Array of corresponding data
            
        Returns:
            Dictionary mapping status to data subset
        """
        result = {}

        unique_statuses = np.unique(statuses)

        for status in unique_statuses:
            if status is np.nan or (isinstance(status, float) and np.isnan(status)):
                continue
            mask = statuses == status
            result[str(status)] = data[mask]

        return result

    @staticmethod
    def group_statistics(group_ids: np.ndarray,
                        values: np.ndarray) -> Dict[str, Dict]:
        """
        Compute statistics per group.
        
        Args:
            group_ids: Array of group identifiers
            values: Array of values
            
        Returns:
            Dictionary mapping group_id -> statistics
        """
        result = {}
        unique_groups = np.unique(group_ids[~pd.isna(group_ids)])

        for group_id in unique_groups:
            mask = group_ids == group_id
            group_values = values[mask]
            clean_values = group_values[~np.isnan(group_values)]

            if len(clean_values) > 0:
                result[str(group_id)] = {
                    "count": len(clean_values),
                    "sum": float(np.sum(clean_values)),
                    "mean": float(np.mean(clean_values)),
                    "median": float(np.median(clean_values)),
                    "std": float(np.std(clean_values)),
                }

        return result


# Import pandas for NotNull check (used in group_statistics)
try:
    import pandas as pd
except ImportError:
    # Fallback if pandas not imported yet
    class MockPD:
        @staticmethod
        def isna(x):
            return x != x or (isinstance(x, float) and np.isnan(x))
    pd = MockPD()
