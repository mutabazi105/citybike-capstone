"""
Main entry point for the CityBike Analytics Platform.
Orchestrates the complete pipeline from data loading to reporting.
"""
import sys
import json
from datetime import datetime

from citybike.analyzer import BikeShareSystem
from citybike.visualization import SummaryDashboard
from citybike.algorithms import ComplexityAnalysis, SortingBenchmark, SearchingBenchmark
from citybike.numerical import StatisticalAnalyzer


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f" {title:^66} ")
    print("=" * 70 + "\n")


def print_section(title: str):
    """Print a section separator."""
    print(f"\n► {title}")
    print("-" * 70)


def main():
    """Main execution pipeline."""

    print_header("CITYBIKE BIKE-SHARING ANALYTICS PLATFORM")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # ====================================================================
    # STEP 1: INITIALIZE SYSTEM
    # ====================================================================
    print_section("Step 1: Initializing System")
    system = BikeShareSystem(data_dir="citybike/data")
    print("✓ BikeShareSystem initialized")

    # ====================================================================
    # STEP 2: LOAD DATA
    # ====================================================================
    print_section("Step 2: Loading Raw Data")
    if not system.load_data():
        print("✗ Failed to load data. Exiting.")
        return False

    print(f"  Trips raw records: {len(system.trips_df)}")
    print(f"  Stations raw records: {len(system.stations_df)}")
    print(f"  Maintenance raw records: {len(system.maintenance_df)}")

    # ====================================================================
    # STEP 3: CLEAN DATA
    # ====================================================================
    print_section("Step 3: Data Cleaning & Validation")
    if not system.clean_data():
        print("✗ Failed to clean data. Exiting.")
        return False

    print("Data quality summary:")
    print(f"  ✓ Removed invalid trips")
    print(f"  ✓ Removed duplicate records")
    print(f"  ✓ Validated coordinates and capacities")
    print(f"  ✓ Converted types (datetime, numeric)")

    # ====================================================================
    # STEP 4: EXPORT CLEANED DATA
    # ====================================================================
    print_section("Step 4: Exporting Cleaned Datasets")
    if system.export_cleaned_data():
        print("  - trips_clean.csv")
        print("  - stations_clean.csv")
        print("  - maintenance_clean.csv")

    # ====================================================================
    # STEP 5: STATISTICAL SUMMARIES (NumPy)
    # ====================================================================
    print_section("Step 5: Numerical Analysis (NumPy)")

    trips = system.trips_clean_df
    durations = trips["duration_minutes"].values
    distances = trips["distance_km"].values

    dur_stats = StatisticalAnalyzer.compute_statistics(durations)
    dist_stats = StatisticalAnalyzer.compute_statistics(distances)

    print("\n📊 TRIP DURATION STATISTICS")
    print(f"  Count:  {dur_stats['count']}")
    print(f"  Mean:   {dur_stats['mean']:.2f} minutes")
    print(f"  Median: {dur_stats['median']:.2f} minutes")
    print(f"  Std:    {dur_stats['std']:.2f} minutes")
    print(f"  Min:    {dur_stats['min']:.2f} minutes")
    print(f"  Max:    {dur_stats['max']:.2f} minutes")
    print(f"  Q25:    {dur_stats['q25']:.2f} minutes")
    print(f"  Q75:    {dur_stats['q75']:.2f} minutes")

    print("\n📊 TRIP DISTANCE STATISTICS")
    print(f"  Count:  {dist_stats['count']}")
    print(f"  Mean:   {dist_stats['mean']:.2f} km")
    print(f"  Median: {dist_stats['median']:.2f} km")
    print(f"  Std:    {dist_stats['std']:.2f} km")
    print(f"  Min:    {dist_stats['min']:.2f} km")
    print(f"  Max:    {dist_stats['max']:.2f} km")
    print(f"  Q25:    {dist_stats['q25']:.2f} km")
    print(f"  Q75:    {dist_stats['q75']:.2f} km")

    # ====================================================================
    # STEP 6: ALGORITHM BENCHMARKING
    # ====================================================================
    print_section("Step 6: Algorithm Benchmarks")

    # Sorting benchmark
    print("\n🔄 SORTING ALGORITHMS")
    print("(Sorting 1000 random numbers by value)")
    test_data = list(range(1000))
    import random
    random.shuffle(test_data)

    sort_times = SortingBenchmark.compare_algorithms(test_data)
    for algo_name, elapsed_time in sorted(sort_times.items(), key=lambda x: x[1]):
        print(f"  {algo_name:15} → {elapsed_time*1000:8.4f} ms")

    # Searching benchmark
    print("\n🔍 SEARCHING ALGORITHMS")
    print("(Searching for random item in 1000 sorted numbers)")
    sorted_test = sorted(test_data)
    target = sorted_test[500]

    search_times = SearchingBenchmark.compare_algorithms(sorted_test, target)
    for algo_name, elapsed_time in sorted(search_times.items(), key=lambda x: x[1]):
        print(f"  {algo_name:15} → {elapsed_time*1000000:8.4f} µs")

    # Complexity analysis
    print("\n📈 ALGORITHM COMPLEXITY (Big-O Analysis)")
    print(ComplexityAnalysis.print_report())

    # ====================================================================
    # STEP 7: BUSINESS ANALYTICS
    # ====================================================================
    print_section("Step 7: Business Analytics (14 Questions)")

    analytics = system.get_all_analytics()

    # Q1: Trip Summary
    q1 = analytics["Q1_summary"]
    print(f"\n1️⃣  TRIP SUMMARY")
    print(f"   Total trips:      {q1['total_trips']}")
    print(f"   Total distance:   {q1['total_distance_km']:.2f} km")
    print(f"   Avg duration:     {q1['average_duration_minutes']:.2f} min")

    # Q2: Popular Stations
    q2 = analytics["Q2_popular_stations"]
    print(f"\n2️⃣  TOP START STATIONS")
    for i, station in enumerate(q2["top_start_stations"][:3], 1):
        print(f"   {i}. {station['station']:25} - {station['trips']} trips")

    # Q4: Peak Day
    q4 = analytics["Q4_peak_day"]
    print(f"\n4️⃣  PEAK DAY")
    print(f"   {q4['peak_day']}, {q4['peak_date']} → {q4['trips']} trips")

    # Q5: Avg Distance by User Type
    q5 = analytics["Q5_avg_distance"]
    print(f"\n5️⃣  AVG DISTANCE BY USER TYPE")
    for user_type, avg_dist in q5.items():
        print(f"   {user_type.title():15} → {avg_dist:.2f} km")

    # Q6: Utilization
    q6 = analytics["Q6_utilization"]
    print(f"\n6️⃣  BIKE UTILIZATION")
    print(f"   Utilization rate: {q6['utilization_percentage']:.2f}%")
    print(f"   Fleet size:       {q6['bikes_in_fleet']} bikes")

    # Q9: Maintenance Cost
    q9 = analytics["Q9_maintenance_cost"]
    print(f"\n9️⃣  MAINTENANCE COST BY BIKE TYPE")
    for bike_type, cost in q9.items():
        print(f"   {bike_type.title():10} → €{cost:.2f}")

    # Q11: Completion Rate
    q11 = analytics["Q11_completion_rate"]
    print(f"\n1️⃣1️⃣ TRIP COMPLETION")
    print(f"   Completion rate: {q11['completion_rate_percentage']:.1f}%")
    print(f"   Completed:       {q11['completed']} trips")
    print(f"   Cancelled:       {q11['cancelled']} trips")

    # Q12: Avg Trips per User
    q12 = analytics["Q12_avg_trips"]
    print(f"\n1️⃣2️⃣ AVG TRIPS PER USER")
    print(f"   Overall:         {q12['overall_average']:.2f} trips/user")
    for user_type, avg in q12["by_user_type"].items():
        print(f"   {user_type.title():15} → {avg:.2f} trips/user")

    print(f"\n   (See full report for all 14 questions)")

    # ====================================================================
    # STEP 8: GENERATE VISUALIZATIONS
    # ====================================================================
    print_section("Step 8: Generating Visualizations")

    dashboard = SummaryDashboard(output_dir="output/figures")
    charts = dashboard.generate_all_charts(
        system.trips_clean_df,
        system.stations_clean_df,
        system.maintenance_clean_df
    )

    dashboard.print_chart_summary(charts)

    # ====================================================================
    # STEP 9: GENERATE SUMMARY REPORT
    # ====================================================================
    print_section("Step 9: Generating Summary Report")

    system.generate_summary_report(output_path="output/summary_report.txt")

    # ====================================================================
    # STEP 10: EXPORT TOP USERS & STATIONS
    # ====================================================================
    print_section("Step 10: Exporting Analysis Results")

    # Top users
    top_users = analytics["Q8_top_users"]
    top_users_df = __import__('pandas').DataFrame(top_users)
    top_users_df.to_csv("output/top_users.csv", index=False)
    print("✓ Exported: output/top_users.csv")

    # Top routes
    top_routes = analytics["Q10_top_routes"]
    top_routes_df = __import__('pandas').DataFrame(top_routes)
    top_routes_df.to_csv("output/top_routes.csv", index=False)
    print("✓ Exported: output/top_routes.csv")

    # ====================================================================
    # COMPLETION MESSAGE
    # ====================================================================
    print_header("ANALYTICS PIPELINE COMPLETE ✓")
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    print("📁 GENERATED FILES:")
    print("  Data/")
    print("    • trips_clean.csv")
    print("    • stations_clean.csv")
    print("    • maintenance_clean.csv")
    print("  Output/")
    print("    • summary_report.txt")
    print("    • top_users.csv")
    print("    • top_routes.csv")
    print("    • figures/")
    print("      - 10+ PNG charts\n")

    print("🎯 NEXT STEPS:")
    print("  1. Review output/summary_report.txt")
    print("  2. Check visualizations in output/figures/")
    print("  3. Push to GitHub with: git push origin feature/oop-models\n")

    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
