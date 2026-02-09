print(" Starting CityBike Data Generation...")
print("=" * 40)

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Set seed for reproducibility
np.random.seed(42)

# Create data directory
os.makedirs("citybike/data", exist_ok=True)

# 1. Generate stations
print("1. Generating stations data...")

station_names = [
    "Central Station", "University Campus", "City Hall", 
    "Riverside Park", "Market Square", "Tech Hub", 
    "Old Town", "Harbor View", "Sports Arena", "West End"
]

stations_data = []
for i, name in enumerate(station_names):
    stations_data.append({
        "station_id": f"ST{100 + i}",
        "station_name": name,
        "capacity": np.random.choice([10, 15, 20, 25]),
        "latitude": round(48.75 + np.random.uniform(0, 0.1), 6),
        "longitude": round(9.15 + np.random.uniform(0, 0.1), 6)
    })

stations_df = pd.DataFrame(stations_data)
stations_df.to_csv("citybike/data/stations.csv", index=False)
print(f"    Created stations.csv with {len(stations_df)} stations")

# 2. Generate trips
print("2. Generating trips data...")

trips_data = []
start_date = datetime(2024, 1, 1)

for i in range(100):  # Start with 100 trips for testing
    user_type = np.random.choice(["casual", "member"], p=[0.3, 0.7])
    bike_type = np.random.choice(["classic", "electric"], p=[0.7, 0.3])
    
    start_time = start_date + timedelta(
        days=np.random.randint(0, 90),
        hours=np.random.randint(6, 21),
        minutes=np.random.randint(0, 60)
    )
    
    duration = np.random.randint(5, 120)
    end_time = start_time + timedelta(minutes=duration)
    distance = round(np.random.uniform(0.5, 10.0), 2)
    
    trips_data.append({
        "trip_id": f"TR{10000 + i}",
        "user_id": f"USR{np.random.randint(1000, 1020)}",
        "user_type": user_type,
        "bike_id": f"BK{np.random.randint(200, 220)}",
        "bike_type": bike_type,
        "start_station_id": np.random.choice(stations_df["station_id"]),
        "end_station_id": np.random.choice(stations_df["station_id"]),
        "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
        "duration_minutes": duration,
        "distance_km": distance,
        "status": np.random.choice(["completed", "cancelled"], p=[0.9, 0.1])
    })

trips_df = pd.DataFrame(trips_data)
trips_df.to_csv("citybike/data/trips.csv", index=False)
print(f"    Created trips.csv with {len(trips_df)} trips")

# 3. Generate maintenance records
print("3. Generating maintenance data...")

maintenance_data = []
maint_types = ["tire_repair", "brake_adjustment", "chain_lubrication", "general_inspection"]

for i in range(30):
    bike_id = f"BK{np.random.randint(200, 220)}"
    maint_type = np.random.choice(maint_types)
    
    # Electric bikes have battery replacement
    if np.random.random() < 0.3:
        bike_type = "electric"
        if np.random.random() < 0.5:
            maint_type = "battery_replacement"
    else:
        bike_type = "classic"
    
    maintenance_data.append({
        "record_id": f"MR{5000 + i}",
        "bike_id": bike_id,
        "bike_type": bike_type,
        "date": (start_date + timedelta(days=np.random.randint(0, 90))).strftime("%Y-%m-%d"),
        "maintenance_type": maint_type,
        "cost": round(np.random.uniform(15, 200), 2),
        "description": f"{maint_type.replace('_', ' ')} for bike {bike_id}"
    })

maintenance_df = pd.DataFrame(maintenance_data)
maintenance_df.to_csv("citybike/data/maintenance.csv", index=False)
print(f"    Created maintenance.csv with {len(maintenance_df)} records")

print("=" * 40)
print(" Data generation complete!")
print(f"\nFiles created in citybike/data/:")
print(f"    stations.csv ({len(stations_df)} records)")
print(f"    trips.csv ({len(trips_df)} records)")
print(f"    maintenance.csv ({len(maintenance_df)} records)")
