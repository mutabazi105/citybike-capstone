"""
Visualization module: Create charts and export visualizations.
Uses Matplotlib to generate all required charts.
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import os
from typing import Dict, List, Optional


class ChartExporter:
    """Base class for creating and exporting charts."""

    def __init__(self, output_dir: str = "output/figures"):
        """
        Initialize chart exporter.

        Args:
            output_dir: Directory to save PNG files
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def save_figure(self, fig, filename: str) -> str:
        """
        Save figure to PNG file.

        Args:
            fig: Matplotlib figure object
            filename: Filename (without .png extension)

        Returns:
            Full path to saved file
        """
        filepath = os.path.join(self.output_dir, f"{filename}.png")
        fig.savefig(filepath, dpi=300, bbox_inches="tight")
        plt.close(fig)
        print(f"✓ Chart saved: {filepath}")
        return filepath

    @staticmethod
    def apply_style():
        """Apply consistent styling to all charts."""
        plt.style.use("seaborn-v0_8-darkgrid")


class TripsAnalyticsCharts(ChartExporter):
    """Create charts for trip analysis."""

    def chart_trips_per_station(self, trips_df: pd.DataFrame,
                                stations_df: pd.DataFrame,
                                top_n: int = 10) -> str:
        """
        Create bar chart: Top stations by trip count.

        Args:
            trips_df: Trips DataFrame
            stations_df: Stations DataFrame
            top_n: Number of top stations to show

        Returns:
            Path to saved figure
        """
        self.apply_style()

        # Count trips per station
        start_counts = trips_df["start_station_id"].value_counts().head(top_n)
        station_names = stations_df.set_index("station_id")["station_name"]

        stations = [station_names.get(sid, sid) for sid in start_counts.index]
        counts = start_counts.values

        # Create chart
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.barh(stations, counts, color="steelblue")

        # Add value labels on bars
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height() / 2,
                    f' {int(width)}',
                    ha='left', va='center', fontweight='bold')

        ax.set_xlabel("Number of Trips", fontsize=12, fontweight='bold')
        ax.set_title(f"Top {top_n} Most Popular Start Stations",
                     fontsize=14, fontweight='bold')
        ax.invert_yaxis()
        fig.tight_layout()

        return self.save_figure(fig, "01_top_stations")

    def chart_monthly_trend(self, trips_df: pd.DataFrame) -> str:
        """
        Create line chart: Monthly trip volume trend.

        Args:
            trips_df: Trips DataFrame

        Returns:
            Path to saved figure
        """
        self.apply_style()

        # Extract month and count trips
        trips_copy = trips_df.copy()
        trips_copy["month"] = trips_copy["start_time"].dt.to_period("M")
        monthly = trips_copy.groupby("month").size()

        # Convert to datetime for proper x-axis
        months = pd.to_datetime(monthly.index.astype(str))
        counts = monthly.values

        # Create chart
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(months, counts, marker='o', linewidth=2.5,
                markersize=8, color="darkgreen")
        ax.fill_between(months, counts, alpha=0.3, color="green")

        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

        ax.set_xlabel("Month", fontsize=12, fontweight='bold')
        ax.set_ylabel("Number of Trips", fontsize=12, fontweight='bold')
        ax.set_title("Monthly Trip Volume Trend",
                     fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        fig.tight_layout()

        return self.save_figure(fig, "02_monthly_trend")

    def chart_duration_distribution(self, trips_df: pd.DataFrame) -> str:
        """
        Create histogram: Trip duration distribution.

        Args:
            trips_df: Trips DataFrame

        Returns:
            Path to saved figure
        """
        self.apply_style()

        durations = trips_df["duration_minutes"].dropna()

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.hist(durations, bins=50, color="coral",
                edgecolor='black', alpha=0.7)

        ax.axvline(durations.mean(), color='red', linestyle='--',
                   linewidth=2, label=f'Mean: {durations.mean():.1f} min')
        ax.axvline(durations.median(), color='blue', linestyle='--',
                   linewidth=2, label=f'Median: {durations.median():.1f} min')

        ax.set_xlabel("Duration (minutes)", fontsize=12, fontweight='bold')
        ax.set_ylabel("Frequency", fontsize=12, fontweight='bold')
        ax.set_title("Trip Duration Distribution",
                     fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3, axis='y')
        fig.tight_layout()

        return self.save_figure(fig, "03_duration_distribution")

    def chart_distance_distribution(self, trips_df: pd.DataFrame) -> str:
        """
        Create histogram: Trip distance distribution.

        Args:
            trips_df: Trips DataFrame

        Returns:
            Path to saved figure
        """
        self.apply_style()

        distances = trips_df["distance_km"].dropna()

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.hist(distances, bins=40, color="skyblue",
                edgecolor='black', alpha=0.7)

        ax.axvline(distances.mean(), color='red', linestyle='--',
                   linewidth=2, label=f'Mean: {distances.mean():.2f} km')
        ax.axvline(distances.median(), color='darkgreen', linestyle='--',
                   linewidth=2, label=f'Median: {distances.median():.2f} km')

        ax.set_xlabel("Distance (km)", fontsize=12, fontweight='bold')
        ax.set_ylabel("Frequency", fontsize=12, fontweight='bold')
        ax.set_title("Trip Distance Distribution",
                     fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3, axis='y')
        fig.tight_layout()

        return self.save_figure(fig, "04_distance_distribution")


class UserAnalyticsCharts(ChartExporter):
    """Create charts for user analysis."""

    def chart_user_type_comparison(self, trips_df: pd.DataFrame) -> str:
        """
        Create box plot: Trip duration by user type.

        Args:
            trips_df: Trips DataFrame

        Returns:
            Path to saved figure
        """
        self.apply_style()

        # Prepare data
        casual_durations = trips_df[trips_df["user_type"]
                                    == "casual"]["duration_minutes"].dropna()
        member_durations = trips_df[trips_df["user_type"]
                                    == "member"]["duration_minutes"].dropna()

        # Create box plot
        fig, ax = plt.subplots(figsize=(10, 6))
        bp = ax.boxplot([casual_durations, member_durations],
                        labels=['Casual Users', 'Member Users'],
                        patch_artist=True,
                        notch=True,
                        showmeans=True)

        # Color the boxes
        colors = ['lightcoral', 'lightgreen']
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)

        ax.set_ylabel("Duration (minutes)", fontsize=12, fontweight='bold')
        ax.set_title("Trip Duration by User Type",
                     fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        fig.tight_layout()

        return self.save_figure(fig, "05_user_type_comparison")

    def chart_bike_type_comparison(self, trips_df: pd.DataFrame) -> str:
        """
        Create box plot: Trip duration by bike type.

        Args:
            trips_df: Trips DataFrame

        Returns:
            Path to saved figure
        """
        self.apply_style()

        # Prepare data
        classic_durations = trips_df[trips_df["bike_type"]
                                     == "classic"]["duration_minutes"].dropna()
        electric_durations = trips_df[trips_df["bike_type"]
                                      == "electric"]["duration_minutes"].dropna()

        # Create box plot
        fig, ax = plt.subplots(figsize=(10, 6))
        bp = ax.boxplot([classic_durations, electric_durations],
                        labels=['Classic Bikes', 'Electric Bikes'],
                        patch_artist=True,
                        notch=True,
                        showmeans=True)

        # Color the boxes
        colors = ['lightyellow', 'lightsteelblue']
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)

        ax.set_ylabel("Duration (minutes)", fontsize=12, fontweight='bold')
        ax.set_title("Trip Duration by Bike Type",
                     fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        fig.tight_layout()

        return self.save_figure(fig, "06_bike_type_comparison")

    def chart_trip_status(self, trips_df: pd.DataFrame) -> str:
        """
        Create pie chart: Trip completion vs cancellation.

        Args:
            trips_df: Trips DataFrame

        Returns:
            Path to saved figure
        """
        self.apply_style()

        # Count by status
        status_counts = trips_df["status"].value_counts()

        # Create pie chart
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#90EE90', '#FFB6C6']
        explode = (0.05, 0.05)

        wedges, texts, autotexts = ax.pie(status_counts.values,
                                          labels=status_counts.index,
                                          autopct='%1.1f%%',
                                          colors=colors,
                                          explode=explode,
                                          startangle=90,
                                          textprops={'fontsize': 12,
                                                     'fontweight': 'bold'})

        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontsize(11)

        ax.set_title("Trip Status Distribution",
                     fontsize=14, fontweight='bold')
        fig.tight_layout()

        return self.save_figure(fig, "07_trip_status")


class MaintenanceAnalyticsCharts(ChartExporter):
    """Create charts for maintenance analysis."""

    def chart_maintenance_cost_by_type(self, maintenance_df: pd.DataFrame) -> str:
        """
        Create bar chart: Maintenance cost by bike type.

        Args:
            maintenance_df: Maintenance DataFrame

        Returns:
            Path to saved figure
        """
        self.apply_style()

        # Sum cost by bike type
        cost_by_type = maintenance_df.groupby(
            "bike_type")["cost"].sum().sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(cost_by_type.index, cost_by_type.values,
                      color=['steelblue', 'coral'])

        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height,
                    f'€{height:.2f}',
                    ha='center', va='bottom', fontweight='bold')

        ax.set_ylabel("Total Cost (€)", fontsize=12, fontweight='bold')
        ax.set_title("Total Maintenance Cost by Bike Type",
                     fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        fig.tight_layout()

        return self.save_figure(fig, "08_maintenance_cost_by_type")

    def chart_maintenance_type_distribution(self, maintenance_df: pd.DataFrame) -> str:
        """
        Create bar chart: Maintenance types frequency.

        Args:
            maintenance_df: Maintenance DataFrame

        Returns:
            Path to saved figure
        """
        self.apply_style()

        # Count by maintenance type
        type_counts = maintenance_df["maintenance_type"].value_counts()

        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.barh(type_counts.index, type_counts.values, color="teal")

        # Add value labels
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height() / 2,
                    f' {int(width)}',
                    ha='left', va='center', fontweight='bold')

        ax.set_xlabel("Number of Records", fontsize=12, fontweight='bold')
        ax.set_title("Maintenance Records by Type",
                     fontsize=14, fontweight='bold')
        ax.invert_yaxis()
        fig.tight_layout()

        return self.save_figure(fig, "09_maintenance_type_distribution")


class PeakHoursChart(ChartExporter):
    """Create charts for peak hour analysis."""

    def chart_hourly_usage(self, trips_df: pd.DataFrame) -> str:
        """
        Create line chart: Hourly usage pattern.

        Args:
            trips_df: Trips DataFrame

        Returns:
            Path to saved figure
        """
        self.apply_style()

        # Extract hour and count trips
        trips_copy = trips_df.copy()
        trips_copy["hour"] = trips_copy["start_time"].dt.hour
        hourly = trips_copy.groupby("hour").size()

        # Create chart
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.plot(hourly.index, hourly.values, marker='o', linewidth=2.5,
                markersize=8, color="darkblue")
        ax.fill_between(hourly.index, hourly.values, alpha=0.3, color="blue")

        # Highlight peak hours (8-9am, 5-7pm)
        peak_hours = [8, 17, 18]
        for hour in peak_hours:
            if hour in hourly.index:
                ax.axvline(hour, color='red', linestyle='--',
                           alpha=0.5, linewidth=1)

        ax.set_xlabel("Hour of Day", fontsize=12, fontweight='bold')
        ax.set_ylabel("Number of Trips", fontsize=12, fontweight='bold')
        ax.set_title("Hourly Usage Pattern (Red lines = Peak Hours)",
                     fontsize=14, fontweight='bold')
        ax.set_xticks(range(0, 24))
        ax.grid(True, alpha=0.3)
        fig.tight_layout()

        return self.save_figure(fig, "10_hourly_usage_pattern")


class SummaryDashboard(ChartExporter):
    """Create summary statistics dashboard."""

    def generate_all_charts(self, trips_df: pd.DataFrame,
                            stations_df: pd.DataFrame,
                            maintenance_df: pd.DataFrame) -> Dict[str, str]:
        """
        Generate all required charts.

        Args:
            trips_df: Trips DataFrame
            stations_df: Stations DataFrame
            maintenance_df: Maintenance DataFrame

        Returns:
            Dictionary mapping chart names to file paths
        """
        charts = {}

        # Trips analytics
        trips_charts = TripsAnalyticsCharts(self.output_dir)
        charts["Top Stations"] = trips_charts.chart_trips_per_station(
            trips_df, stations_df
        )
        charts["Monthly Trend"] = trips_charts.chart_monthly_trend(trips_df)
        charts["Duration Distribution"] = trips_charts.chart_duration_distribution(
            trips_df)
        charts["Distance Distribution"] = trips_charts.chart_distance_distribution(
            trips_df)

        # User analytics
        user_charts = UserAnalyticsCharts(self.output_dir)
        charts["User Type Comparison"] = user_charts.chart_user_type_comparison(
            trips_df)
        charts["Bike Type Comparison"] = user_charts.chart_bike_type_comparison(
            trips_df)
        charts["Trip Status"] = user_charts.chart_trip_status(trips_df)

        # Maintenance analytics
        maint_charts = MaintenanceAnalyticsCharts(self.output_dir)
        charts["Maintenance Cost by Type"] = maint_charts.chart_maintenance_cost_by_type(
            maintenance_df
        )
        charts["Maintenance Type Distribution"] = maint_charts.chart_maintenance_type_distribution(
            maintenance_df
        )

        # Peak hours
        peak_charts = PeakHoursChart(self.output_dir)
        charts["Hourly Usage Pattern"] = peak_charts.chart_hourly_usage(
            trips_df)

        print(f"\n✓ Generated {len(charts)} charts successfully")

        return charts

    def print_chart_summary(self, charts: Dict[str, str]):
        """Print summary of generated charts."""
        print("\n" + "=" * 70)
        print("CHARTS GENERATED")
        print("=" * 70)
        for i, (name, path) in enumerate(charts.items(), 1):
            print(f"{i:2}. {name:<30} → {os.path.basename(path)}")
        print("=" * 70)
