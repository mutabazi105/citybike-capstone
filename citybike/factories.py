"""
Factory functions to create domain objects from CSV data.
Implements the Factory Pattern for data instantiation.
"""
from datetime import datetime
from typing import Dict, List, Optional
from .models import (
    ClassicBike, ElectricBike, Station,
    CasualUser, MemberUser, Trip, MaintenanceRecord
)


def parse_datetime(date_string: str) -> datetime:
    """Parse datetime string from CSV."""
    return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")


def create_bike(bike_id: str, bike_type: str, status: str = "available"):
    """
    Factory function to create a bike based on type.

    Args:
        bike_id: Unique bike identifier
        bike_type: "classic" or "electric"
        status: Current status

    Returns:
        ClassicBike or ElectricBike instance

    Raises:
        ValueError: If bike_type is invalid
    """
    if bike_type == "classic":
        return ClassicBike(bike_id, gear_count=21, status=status)
    elif bike_type == "electric":
        return ElectricBike(bike_id, battery_level=100,
                            max_range_km=50, status=status)
    else:
        raise ValueError(f"Unknown bike type: {bike_type}")


def create_station(row: Dict) -> Station:
    """
    Factory function to create a Station from CSV row.

    Args:
        row: Dictionary with keys: station_id, station_name, capacity, 
             latitude, longitude

    Returns:
        Station instance
    """
    return Station(
        station_id=row["station_id"],
        name=row["station_name"],
        capacity=int(row["capacity"]),
        latitude=float(row["latitude"]),
        longitude=float(row["longitude"])
    )


def create_user(user_id: str, user_type: str, name: str = "Unknown",
                email: str = "unknown@city-bike.local") -> CasualUser | MemberUser:
    """
    Factory function to create a user based on type.

    Args:
        user_id: Unique user identifier
        user_type: "casual" or "member"
        name: User's name
        email: User's email address

    Returns:
        CasualUser or MemberUser instance

    Raises:
        ValueError: If user_type is invalid
    """
    if user_type == "casual":
        return CasualUser(user_id, name, email, day_pass_count=5)
    elif user_type == "member":
        start = datetime.now()
        from datetime import timedelta
        end = start + timedelta(days=365)
        return MemberUser(user_id, name, email, start, end, tier="basic")
    else:
        raise ValueError(f"Unknown user type: {user_type}")


def create_trip(row: Dict, users_cache: Dict, bikes_cache: Dict,
                stations_cache: Dict) -> Optional[Trip]:
    """
    Factory function to create a Trip from CSV row.

    Args:
        row: Trip CSV row data
        users_cache: Dictionary of user_id -> User objects
        bikes_cache: Dictionary of bike_id -> Bike objects
        stations_cache: Dictionary of station_id -> Station objects

    Returns:
        Trip instance or None if objects not found in cache
    """
    # Get objects from cache
    user = users_cache.get(row["user_id"])
    bike = bikes_cache.get(row["bike_id"])
    start_station = stations_cache.get(row["start_station_id"])
    end_station = stations_cache.get(row["end_station_id"])

    if not all([user, bike, start_station, end_station]):
        return None  # Skip if any required object is missing

    return Trip(
        trip_id=row["trip_id"],
        user=user,
        bike=bike,
        start_station=start_station,
        end_station=end_station,
        start_time=parse_datetime(row["start_time"]),
        end_time=parse_datetime(row["end_time"]),
        distance_km=float(row["distance_km"])
    )


def create_maintenance_record(row: Dict, bikes_cache: Dict) -> Optional[MaintenanceRecord]:
    """
    Factory function to create a MaintenanceRecord from CSV row.

    Args:
        row: Maintenance CSV row data
        bikes_cache: Dictionary of bike_id -> Bike objects

    Returns:
        MaintenanceRecord instance or None if bike not found
    """
    bike = bikes_cache.get(row["bike_id"])
    if not bike:
        return None  # Skip if bike not found

    return MaintenanceRecord(
        record_id=row["record_id"],
        bike=bike,
        date=datetime.strptime(row["date"], "%Y-%m-%d"),
        maintenance_type=row["maintenance_type"],
        cost=float(row["cost"]),
        description=row.get("description", "")
    )


# Cache storage for reusable objects
class DataCache:
    """Thread-safe cache for storing created objects."""

    def __init__(self):
        self.users = {}
        self.bikes = {}
        self.stations = {}
        self.trips = {}
        self.maintenance = {}

    def add_user(self, user_id: str, user):
        """Add user to cache."""
        self.users[user_id] = user

    def add_bike(self, bike_id: str, bike):
        """Add bike to cache."""
        self.bikes[bike_id] = bike

    def add_station(self, station_id: str, station):
        """Add station to cache."""
        self.stations[station_id] = station

    def add_trip(self, trip_id: str, trip):
        """Add trip to cache."""
        self.trips[trip_id] = trip

    def add_maintenance(self, record_id: str, record):
        """Add maintenance record to cache."""
        self.maintenance[record_id] = record

    def get_all_users(self) -> List:
        """Get all cached users."""
        return list(self.users.values())

    def get_all_bikes(self) -> List:
        """Get all cached bikes."""
        return list(self.bikes.values())

    def get_all_stations(self) -> List:
        """Get all cached stations."""
        return list(self.stations.values())

    def get_all_trips(self) -> List:
        """Get all cached trips."""
        return list(self.trips.values())

    def get_all_maintenance(self) -> List:
        """Get all cached maintenance records."""
        return list(self.maintenance.values())

    def clear(self):
        """Clear all caches."""
        self.users.clear()
        self.bikes.clear()
        self.stations.clear()
        self.trips.clear()
        self.maintenance.clear()
