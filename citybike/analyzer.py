"""
Data analysis module: Load, clean, and analyze bike-sharing data.
Central orchestrator for data operations and business analytics.
"""
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
import os

from .factories import DataCache, create_bike, create_station, create_user, create_trip, create_maintenance_record
from .models import Trip, MaintenanceRecord, Bike, Station, User
from .numerical import StatisticalAnalyzer, OutlierDetection, DistanceCalculator
from .pricing import PricingFactory, TripFareCalculator
from .utils import parse_datetime, parse_date


class DataCleaner:
    """Clean and validate raw data from CSV files."""

    @staticmethod
    def clean_trips_csv(df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean trips data.

        Args:
            df: Raw trips DataFrame

        Returns:
            Cleaned DataFrame
        """
        df = df.copy()

        # Convert datetime columns
        df["start_time"] = pd.to_datetime(df["start_time"], errors="coerce")
        df["end_time"] = pd.to_datetime(df["end_time"], errors="coerce")

        # Convert numeric columns
        df["duration_minutes"] = pd.to_numeric(
            df["duration_minutes"], errors="coerce")
        df["distance_km"] = pd.to_numeric(df["distance_km"], errors="coerce")

        # Remove rows where end_time is before start_time
        invalid_times = df["end_time"] < df["start_time"]
        df = df[~invalid_times]

        # Remove duplicate rows
        df = df.drop_duplicates(subset=["trip_id"], keep="first")

        # Remove rows with missing critical columns
        df = df.dropna(subset=["trip_id", "user_id", "bike_id",
                               "start_station_id", "end_station_id"])

        # Handle missing durations by calculating from timestamps
        if df["duration_minutes"].isna().any():
            mask = df["duration_minutes"].isna()
            df.loc[mask, "duration_minutes"] = (
                (df.loc[mask, "end_time"] -
                 df.loc[mask, "start_time"]).dt.total_seconds() / 60
            )

        # Remove rows with still-missing duration (< 1 minute probably invalid)
        df = df.dropna(subset=["duration_minutes"])
        df = df[df["duration_minutes"] >= 1]

        # Handle missing distances (fill with mean)
        if df["distance_km"].isna().any():
            mean_distance = df["distance_km"].mean()
            df["distance_km"].fillna(mean_distance, inplace=True)

        # Validate status column
        valid_statuses = {"completed", "cancelled"}
        df = df[df["status"].isin(valid_statuses) | df["status"].isna()]

        return df

    @staticmethod
    def clean_stations_csv(df: pd.DataFrame) -> pd.DataFrame:
        """Clean stations data."""
        df = df.copy()

        # Convert numeric columns
        df["capacity"] = pd.to_numeric(df["capacity"], errors="coerce")
        df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
        df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

        # Remove duplicates
        df = df.drop_duplicates(subset=["station_id"], keep="first")

        # Remove rows with missing critical fields
        df = df.dropna(subset=["station_id", "station_name",
                               "capacity", "latitude", "longitude"])

        # Validate coordinates
        df = df[(df["latitude"] >= -90) &
                (df["latitude"] <= 90) &
                (df["longitude"] >= -180) &
                (df["longitude"] <= 180)]

        # Validate capacity (> 0)
        df = df[df["capacity"] > 0]

        return df

    @staticmethod
    def clean_maintenance_csv(df: pd.DataFrame) -> pd.DataFrame:
        """Clean maintenance data."""
        df = df.copy()

        # Parse date
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

        # Convert cost
        df["cost"] = pd.to_numeric(df["cost"], errors="coerce")

        # Remove duplicates
        df = df.drop_duplicates(subset=["record_id"], keep="first")

        # Remove rows with missing critical fields
        df = df.dropna(subset=["record_id", "bike_id", "date",
                               "maintenance_type", "cost"])

        # Validate maintenance type
        valid_types = {
            "tire_repair", "brake_adjustment", "battery_replacement",
            "chain_lubrication", "general_inspection"
        }
        df = df[df["maintenance_type"].isin(valid_types)]

        # Validate cost (>= 0)
        df = df[df["cost"] >= 0]

        return df


class BikeShareSystem:
    """
    Main orchestrator for bike-sharing system analysis.
    Handles data loading, cleaning, and all business analytics.
    """

    def __init__(self, data_dir: str = "citybike/data"):
        """
        Initialize the system.

        Args:
            data_dir: Directory containing CSV files
        """
        self.data_dir = data_dir
        self.cache = DataCache()

        # DataFrames
        self.trips_df = None
        self.stations_df = None
        self.maintenance_df = None

        # Cleaned versions
        self.trips_clean_df = None
        self.stations_clean_df = None
        self.maintenance_clean_df = None

    def load_data(self) -> bool:
        """
        Load raw CSV data.

        Returns:
            True if successful
        """
        try:
            self.trips_df = pd.read_csv(
                os.path.join(self.data_dir, "trips.csv")
            )
            self.stations_df = pd.read_csv(
                os.path.join(self.data_dir, "stations.csv")
            )
            self.maintenance_df = pd.read_csv(
                os.path.join(self.data_dir, "maintenance.csv")
            )
            print("✓ Data loaded successfully")
            return True
        except Exception as e:
            print(f"✗ Error loading data: {e}")
            return False

    def clean_data(self) -> bool:
        """
        Clean and validate all datasets.

        Returns:
            True if successful
        """
        try:
            cleaner = DataCleaner()

            self.trips_clean_df = cleaner.clean_trips_csv(self.trips_df)
            self.stations_clean_df = cleaner.clean_stations_csv(
                self.stations_df)
            self.maintenance_clean_df = cleaner.clean_maintenance_csv(
                self.maintenance_df
            )

            print("✓ Data cleaned successfully")
            print(f"  - Trips: {len(self.trips_clean_df)} records")
            print(f"  - Stations: {len(self.stations_clean_df)} records")
            print(f"  - Maintenance: {len(self.maintenance_clean_df)} records")

            return True
        except Exception as e:
            print(f"✗ Error cleaning data: {e}")
            return False

    def export_cleaned_data(self, output_dir: str = "citybike/data") -> bool:
        """Export cleaned datasets to CSV."""
        try:
            self.trips_clean_df.to_csv(
                os.path.join(output_dir, "trips_clean.csv"),
                index=False
            )
            self.stations_clean_df.to_csv(
                os.path.join(output_dir, "stations_clean.csv"),
                index=False
            )
            self.maintenance_clean_df.to_csv(
                os.path.join(output_dir, "maintenance_clean.csv"),
                index=False
            )
            print("✓ Cleaned data exported")
            return True
        except Exception as e:
            print(f"✗ Error exporting data: {e}")
            return False

    # ====================================================================
    # BUSINESS ANALYTICS - 10+ QUESTIONS
    # ====================================================================

    def q1_trip_summary(self) -> Dict[str, Any]:
        """Q1: Total trips, distance, average duration."""
        trips = self.trips_clean_df

        total_trips = len(trips)
        total_distance = trips["distance_km"].sum()
        avg_duration = trips["duration_minutes"].mean()

        return {
            "total_trips": total_trips,
            "total_distance_km": round(total_distance, 2),
            "average_duration_minutes": round(avg_duration, 2),
        }

    def q2_popular_stations(self, top_n: int = 10) -> Dict[str, List]:
        """Q2: Top N most popular start and end stations."""
        trips = self.trips_clean_df
        stations = self.stations_clean_df

        start_counts = trips["start_station_id"].value_counts().head(top_n)
        end_counts = trips["end_station_id"].value_counts().head(top_n)

        # Map station IDs to names
        station_map = dict(zip(stations["station_id"],
                               stations["station_name"]))

        top_starts = [
            {"station": station_map.get(sid, sid), "trips": int(count)}
            for sid, count in start_counts.items()
        ]

        top_ends = [
            {"station": station_map.get(sid, sid), "trips": int(count)}
            for sid, count in end_counts.items()
        ]

        return {
            "top_start_stations": top_starts,
            "top_end_stations": top_ends,
        }

    def q3_peak_hours(self) -> Dict[int, int]:
        """Q3: Peak usage hours during day."""
        trips = self.trips_clean_df
        trips_copy = trips.copy()
        trips_copy["hour"] = trips_copy["start_time"].dt.hour

        hourly_counts = trips_copy.groupby("hour").size()

        return {
            int(hour): int(count)
            for hour, count in hourly_counts.items()
        }

    def q4_peak_day(self) -> Dict[str, Any]:
        """Q4: Day with highest trip volume."""
        trips = self.trips_clean_df
        trips_copy = trips.copy()
        trips_copy["date"] = trips_copy["start_time"].dt.date
        trips_copy["day_of_week"] = trips_copy["start_time"].dt.day_name()

        daily_counts = trips_copy.groupby(["date", "day_of_week"]).size()

        if len(daily_counts) > 0:
            peak_entry = daily_counts.idxmax()
            peak_date, peak_day = peak_entry
            peak_trips = int(daily_counts.max())
        else:
            return {"peak_date": None, "peak_day": None, "trips": 0}

        return {
            "peak_date": str(peak_date),
            "peak_day": peak_day,
            "trips": peak_trips,
        }

    def q5_avg_distance_by_user_type(self) -> Dict[str, float]:
        """Q5: Average distance by user type."""
        trips = self.trips_clean_df

        avg_by_type = trips.groupby("user_type")["distance_km"].mean()

        return {
            user_type: round(avg_dist, 2)
            for user_type, avg_dist in avg_by_type.items()
        }

    def q6_bike_utilization(self) -> Dict[str, Any]:
        """Q6: Bike utilization rate."""
        trips = self.trips_clean_df
        bikes = self.trips_clean_df["bike_id"].nunique()

        # Rough estimate: total usage minutes / (bikes * 24 * 60 * days)
        date_range = (
            trips["start_time"].max() - trips["start_time"].min()
        ).days + 1

        total_possible_minutes = bikes * 24 * 60 * date_range
        total_usage_minutes = trips["duration_minutes"].sum()

        utilization_rate = (
            (total_usage_minutes / total_possible_minutes * 100)
            if total_possible_minutes > 0 else 0
        )

        return {
            "utilization_percentage": round(utilization_rate, 2),
            "bikes_in_fleet": bikes,
            "date_range_days": date_range,
        }

    def q7_monthly_trend(self) -> Dict[str, int]:
        """Q7: Monthly trip trend."""
        trips = self.trips_clean_df
        trips_copy = trips.copy()
        trips_copy["month"] = trips_copy["start_time"].dt.to_period("M")

        monthly_counts = trips_copy.groupby("month").size()

        return {
            str(month): int(count)
            for month, count in monthly_counts.items()
        }

    def q8_top_users(self, top_n: int = 15) -> List[Dict]:
        """Q8: Top N most active users."""
        trips = self.trips_clean_df

        user_trip_counts = trips["user_id"].value_counts().head(top_n)

        return [
            {"user_id": uid, "trip_count": int(count)}
            for uid, count in user_trip_counts.items()
        ]

    def q9_maintenance_cost_by_type(self) -> Dict[str, float]:
        """Q9: Total maintenance cost per bike type."""
        maint = self.maintenance_clean_df

        cost_by_type = maint.groupby("bike_type")["cost"].sum()

        return {
            bike_type: round(cost, 2)
            for bike_type, cost in cost_by_type.items()
        }

    def q10_top_routes(self, top_n: int = 10) -> List[Dict]:
        """Q10: Top origin-destination pairs."""
        trips = self.trips_clean_df
        stations = self.stations_clean_df

        station_map = dict(zip(stations["station_id"],
                               stations["station_name"]))

        route_counts = trips.groupby(
            ["start_station_id", "end_station_id"]
        ).size().sort_values(ascending=False).head(top_n)

        top_routes = []
        for (start_id, end_id), count in route_counts.items():
            top_routes.append({
                "start_station": station_map.get(start_id, start_id),
                "end_station": station_map.get(end_id, end_id),
                "total_trips": int(count),
            })

        return top_routes

    def q11_trip_completion_rate(self) -> Dict[str, Any]:
        """Q11: Trip completion rate."""
        trips = self.trips_clean_df

        total = len(trips)
        completed = len(trips[trips["status"] == "completed"])
        cancelled = len(trips[trips["status"] == "cancelled"])

        completion_rate = (completed / total * 100) if total > 0 else 0

        return {
            "completion_rate_percentage": round(completion_rate, 2),
            "total_trips": total,
            "completed": completed,
            "cancelled": cancelled,
        }

    def q12_avg_trips_per_user(self) -> Dict[str, Any]:
        """Q12: Average trips per user, by type."""
        trips = self.trips_clean_df

        by_user_type = trips.groupby("user_type").apply(
            lambda g: len(g) / g["user_id"].nunique()
        )

        total_users = trips["user_id"].nunique()
        total_trips = len(trips)
        avg_overall = total_trips / total_users if total_users > 0 else 0

        return {
            "overall_average": round(avg_overall, 2),
            "by_user_type": {
                user_type: round(avg, 2)
                for user_type, avg in by_user_type.items()
            },
        }

    def q13_bike_maintenance_frequency(self, top_n: int = 10) -> List[Dict]:
        """Q13: Bikes with highest maintenance frequency."""
        maint = self.maintenance_clean_df

        maint_counts = maint["bike_id"].value_counts().head(top_n)

        return [
            {"bike_id": bid, "maintenance_records": int(count)}
            for bid, count in maint_counts.items()
        ]

    def q14_outlier_trips(self) -> Dict[str, List]:
        """Q14: Outlier trips (unusual duration/distance)."""
        trips = self.trips_clean_df

        # Detect outliers using IQR method
        durations = trips["duration_minutes"].values
        distances = trips["distance_km"].values

        outlier_duration, bounds_d = OutlierDetection.iqr_outliers(durations)
        outlier_distance, bounds_k = OutlierDetection.iqr_outliers(distances)

        outliers = trips[outlier_duration | outlier_distance]

        outlier_list = [
            {
                "trip_id": tid,
                "duration_minutes": float(dur),
                "distance_km": float(dist),
            }
            for tid, dur, dist in zip(
                outliers["trip_id"],
                outliers["duration_minutes"],
                outliers["distance_km"],
            )
        ]

        return {
            "total_outliers": len(outlier_list),
            "outliers": outlier_list[:20],  # Top 20
        }

    # Additional helper methods

    def get_all_analytics(self) -> Dict[str, Any]:
        """Get all business analytics results."""
        return {
            "Q1_summary": self.q1_trip_summary(),
            "Q2_popular_stations": self.q2_popular_stations(),
            "Q3_peak_hours": self.q3_peak_hours(),
            "Q4_peak_day": self.q4_peak_day(),
            "Q5_avg_distance": self.q5_avg_distance_by_user_type(),
            "Q6_utilization": self.q6_bike_utilization(),
            "Q7_monthly_trend": self.q7_monthly_trend(),
            "Q8_top_users": self.q8_top_users(),
            "Q9_maintenance_cost": self.q9_maintenance_cost_by_type(),
            "Q10_top_routes": self.q10_top_routes(),
            "Q11_completion_rate": self.q11_trip_completion_rate(),
            "Q12_avg_trips": self.q12_avg_trips_per_user(),
            "Q13_maintenance_freq": self.q13_bike_maintenance_frequency(),
            "Q14_outliers": self.q14_outlier_trips(),
        }

    def generate_summary_report(self, output_path: str = "output/summary_report.txt"):
        """Generate a text report with all findings."""
        analytics = self.get_all_analytics()

        report = self._format_report(analytics)

        # Create output directory if needed
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w") as f:
            f.write(report)

        print(f"✓ Report generated: {output_path}")
        return report

    def _format_report(self, analytics: Dict) -> str:
        """Format analytics into readable report."""
        report = """
================================================================================
BIKE-SHARING SYSTEM: ANALYTICS REPORT
================================================================================
Report Generated: {}

""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        # Q1: Trip Summary
        q1 = analytics["Q1_summary"]
        report += """
Q1: TRIP SUMMARY
================
Total Trips: {}
Total Distance: {} km
Average Duration: {} minutes

""".format(q1["total_trips"], q1["total_distance_km"],
           q1["average_duration_minutes"])

        # Q2: Popular Stations
        q2 = analytics["Q2_popular_stations"]
        report += """
Q2: TOP 10 START STATIONS
=========================
"""
        for i, station in enumerate(q2["top_start_stations"], 1):
            report += "{:2}. {} - {} trips\n".format(
                i, station["station"], station["trips"]
            )

        report += """
Q2: TOP 10 END STATIONS
=======================
"""
        for i, station in enumerate(q2["top_end_stations"], 1):
            report += "{:2}. {} - {} trips\n".format(
                i, station["station"], station["trips"]
            )

        # Q6: Utilization
        q6 = analytics["Q6_utilization"]
        report += """
Q6: BIKE UTILIZATION
====================
Utilization Rate: {}%
Fleet Size: {} bikes
Date Range: {} days

""".format(q6["utilization_percentage"], q6["bikes_in_fleet"],
           q6["date_range_days"])

        # Q11: Completion Rate
        q11 = analytics["Q11_completion_rate"]
        report += """
Q11: TRIP COMPLETION
====================
Completion Rate: {}%
Completed: {} trips
Cancelled: {} trips

""".format(q11["completion_rate_percentage"],
           q11["completed"], q11["cancelled"])

        return report
