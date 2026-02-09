"""
Domain models for the CityBike system.
Contains all entity classes with proper OOP design.
"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Union
import re


class Entity(ABC):
    """Abstract base class for all entities."""

    def __init__(self, entity_id: str):
        """
        Initialize an entity.

        Args:
            entity_id: Unique identifier for the entity

        Raises:
            ValueError: If entity_id is empty or None
        """
        if not entity_id or not isinstance(entity_id, str):
            raise ValueError("Entity ID must be a non-empty string")

        self._id = entity_id
        self._created_at = datetime.now()

    @property
    def id(self) -> str:
        """Get the entity ID."""
        return self._id

    @property
    def created_at(self) -> datetime:
        """Get the creation timestamp."""
        return self._created_at

    @abstractmethod
    def __str__(self) -> str:
        """User-friendly string representation."""
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """Developer-friendly string representation for debugging."""
        pass


class Bike(Entity):
    """Base class for all bikes."""

    VALID_STATUSES = {"available", "in_use", "maintenance"}

    def __init__(self, bike_id: str, bike_type: str, status: str = "available"):
        """
        Initialize a bike.

        Args:
            bike_id: Unique bike identifier
            bike_type: Type of bike (classic/electric)
            status: Current status of the bike

        Raises:
            ValueError: If invalid parameters provided
        """
        super().__init__(bike_id)

        if not bike_type or not isinstance(bike_type, str):
            raise ValueError("Bike type must be a non-empty string")

        if status not in self.VALID_STATUSES:
            raise ValueError(f"Status must be one of {self.VALID_STATUSES}")

        self._bike_type = bike_type
        self._status = status

    @property
    def bike_type(self) -> str:
        """Get the bike type."""
        return self._bike_type

    @property
    def status(self) -> str:
        """Get the current status."""
        return self._status

    @status.setter
    def status(self, new_status: str):
        """Set the bike status with validation."""
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Status must be one of {self.VALID_STATUSES}")
        self._status = new_status

    def __str__(self) -> str:
        return f"{self.bike_type.title()} Bike {self.id} ({self.status})"

    def __repr__(self) -> str:
        return f"Bike(id={self.id!r}, type={self.bike_type!r}, status={self.status!r})"


class ClassicBike(Bike):
    """Classic (non-electric) bike."""

    def __init__(self, bike_id: str, gear_count: int, status: str = "available"):
        """
        Initialize a classic bike.

        Args:
            bike_id: Unique bike identifier
            gear_count: Number of gears (1-21)
            status: Current status

        Raises:
            ValueError: If gear_count is invalid
        """
        super().__init__(bike_id, "classic", status)

        if not isinstance(gear_count, int) or gear_count < 1 or gear_count > 21:
            raise ValueError("Gear count must be between 1 and 21")

        self._gear_count = gear_count

    @property
    def gear_count(self) -> int:
        """Get the number of gears."""
        return self._gear_count

    def __str__(self) -> str:
        return f"Classic Bike {self.id} with {self.gear_count} gears ({self.status})"

    def __repr__(self) -> str:
        return (f"ClassicBike(id={self.id!r}, gears={self.gear_count}, "
                f"status={self.status!r})")


class ElectricBike(Bike):
    """Electric bike with battery."""

    def __init__(self, bike_id: str, battery_level: float,
                 max_range_km: float, status: str = "available"):
        """
        Initialize an electric bike.

        Args:
            bike_id: Unique bike identifier
            battery_level: Current battery level (0-100%)
            max_range_km: Maximum range on full charge
            status: Current status

        Raises:
            ValueError: If invalid parameters provided
        """
        super().__init__(bike_id, "electric", status)

        if not 0 <= battery_level <= 100:
            raise ValueError("Battery level must be between 0 and 100")

        if max_range_km <= 0:
            raise ValueError("Maximum range must be positive")

        self._battery_level = battery_level
        self._max_range_km = max_range_km

    @property
    def battery_level(self) -> float:
        """Get current battery level (0-100%)."""
        return self._battery_level

    @battery_level.setter
    def battery_level(self, level: float):
        """Set battery level with validation."""
        if not 0 <= level <= 100:
            raise ValueError("Battery level must be between 0 and 100")
        self._battery_level = level

    @property
    def max_range_km(self) -> float:
        """Get maximum range on full charge."""
        return self._max_range_km

    def estimated_range(self) -> float:
        """Calculate estimated range based on current battery."""
        return (self.battery_level / 100) * self.max_range_km

    def __str__(self) -> str:
        return (f"Electric Bike {self.id} - {self.battery_level}% battery "
                f"({self.status})")

    def __repr__(self) -> str:
        return (f"ElectricBike(id={self.id!r}, battery={self.battery_level}%, "
                f"max_range={self.max_range_km}km, status={self.status!r})")


class Station(Entity):
    """Bike station with location and capacity."""

    def __init__(self, station_id: str, name: str, capacity: int,
                 latitude: float, longitude: float):
        """
        Initialize a station.

        Args:
            station_id: Unique station identifier
            name: Station name
            capacity: Maximum number of bikes
            latitude: Geographic latitude
            longitude: Geographic longitude

        Raises:
            ValueError: If invalid parameters provided
        """
        super().__init__(station_id)

        if not name or not isinstance(name, str):
            raise ValueError("Station name must be a non-empty string")

        if not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("Capacity must be a positive integer")

        if not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")

        if not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")

        self._name = name
        self._capacity = capacity
        self._latitude = latitude
        self._longitude = longitude
        self._current_bikes = []  # List of bike IDs currently at station

    @property
    def name(self) -> str:
        """Get station name."""
        return self._name

    @property
    def capacity(self) -> int:
        """Get station capacity."""
        return self._capacity

    @property
    def latitude(self) -> float:
        """Get station latitude."""
        return self._latitude

    @property
    def longitude(self) -> float:
        """Get station longitude."""
        return self._longitude

    @property
    def available_spots(self) -> int:
        """Calculate available spots at the station."""
        return max(0, self.capacity - len(self._current_bikes))

    def add_bike(self, bike_id: str) -> bool:
        """Add a bike to the station if space available."""
        if len(self._current_bikes) < self.capacity and bike_id not in self._current_bikes:
            self._current_bikes.append(bike_id)
            return True
        return False

    def remove_bike(self, bike_id: str) -> bool:
        """Remove a bike from the station."""
        if bike_id in self._current_bikes:
            self._current_bikes.remove(bike_id)
            return True
        return False

    def __str__(self) -> str:
        return f"{self.name} Station ({len(self._current_bikes)}/{self.capacity} bikes)"

    def __repr__(self) -> str:
        return (f"Station(id={self.id!r}, name={self.name!r}, "
                f"capacity={self.capacity}, lat={self.latitude}, "
                f"lon={self.longitude})")


class User(Entity):
    """Base class for all users."""

    EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    def __init__(self, user_id: str, name: str, email: str, user_type: str):
        """
        Initialize a user.

        Args:
            user_id: Unique user identifier
            name: User's name
            email: User's email address
            user_type: Type of user (casual/member)

        Raises:
            ValueError: If invalid parameters provided
        """
        super().__init__(user_id)

        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string")

        if not email or not isinstance(email, str):
            raise ValueError("Email must be a non-empty string")

        if not re.match(self.EMAIL_REGEX, email):
            raise ValueError("Invalid email format")

        if user_type not in {"casual", "member"}:
            raise ValueError("User type must be 'casual' or 'member'")

        self._name = name
        self._email = email
        self._user_type = user_type

    @property
    def name(self) -> str:
        """Get user's name."""
        return self._name

    @property
    def email(self) -> str:
        """Get user's email."""
        return self._email

    @property
    def user_type(self) -> str:
        """Get user type."""
        return self._user_type

    def __str__(self) -> str:
        return f"{self.name} ({self.user_type} user)"

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, type={self.user_type!r})"


class CasualUser(User):
    """Casual user (pay-per-ride or day pass)."""

    def __init__(self, user_id: str, name: str, email: str,
                 day_pass_count: int = 0):
        """
        Initialize a casual user.

        Args:
            user_id: Unique user identifier
            name: User's name
            email: User's email
            day_pass_count: Number of day passes purchased

        Raises:
            ValueError: If day_pass_count is negative
        """
        super().__init__(user_id, name, email, "casual")

        if day_pass_count < 0:
            raise ValueError("Day pass count cannot be negative")

        self._day_pass_count = day_pass_count

    @property
    def day_pass_count(self) -> int:
        """Get number of day passes."""
        return self._day_pass_count

    def add_day_pass(self, count: int = 1):
        """Add day passes."""
        if count <= 0:
            raise ValueError("Must add at least 1 day pass")
        self._day_pass_count += count

    def use_day_pass(self):
        """Use a day pass if available."""
        if self._day_pass_count > 0:
            self._day_pass_count -= 1
            return True
        return False

    def __str__(self) -> str:
        return f"{self.name} (Casual - {self.day_pass_count} day passes)"

    def __repr__(self) -> str:
        return (f"CasualUser(id={self.id!r}, name={self.name!r}, "
                f"day_passes={self.day_pass_count})")


class MemberUser(User):
    """Member user with subscription."""

    VALID_TIERS = {"basic", "premium"}

    def __init__(self, user_id: str, name: str, email: str,
                 membership_start: datetime, membership_end: datetime,
                 tier: str = "basic"):
        """
        Initialize a member user.

        Args:
            user_id: Unique user identifier
            name: User's name
            email: User's email
            membership_start: Start date of membership
            membership_end: End date of membership
            tier: Membership tier (basic/premium)

        Raises:
            ValueError: If invalid parameters provided
        """
        super().__init__(user_id, name, email, "member")

        if not isinstance(membership_start, datetime):
            raise ValueError("membership_start must be a datetime object")

        if not isinstance(membership_end, datetime):
            raise ValueError("membership_end must be a datetime object")

        if membership_end <= membership_start:
            raise ValueError("membership_end must be after membership_start")

        if tier not in self.VALID_TIERS:
            raise ValueError(f"Tier must be one of {self.VALID_TIERS}")

        self._membership_start = membership_start
        self._membership_end = membership_end
        self._tier = tier

    @property
    def membership_start(self) -> datetime:
        """Get membership start date."""
        return self._membership_start

    @property
    def membership_end(self) -> datetime:
        """Get membership end date."""
        return self._membership_end

    @property
    def tier(self) -> str:
        """Get membership tier."""
        return self._tier

    def is_active(self) -> bool:
        """Check if membership is currently active."""
        now = datetime.now()
        return self._membership_start <= now <= self._membership_end

    def days_remaining(self) -> int:
        """Calculate days remaining in membership."""
        if not self.is_active():
            return 0
        return (self._membership_end - datetime.now()).days

    def __str__(self) -> str:
        status = "Active" if self.is_active() else "Expired"
        return f"{self.name} ({self.tier.title()} Member - {status})"

    def __repr__(self) -> str:
        return (f"MemberUser(id={self.id!r}, name={self.name!r}, "
                f"tier={self.tier!r}, active={self.is_active()})")


class Trip(Entity):
    """Represents a bike trip."""

    def __init__(self, trip_id: str, user: User, bike: Bike,
                 start_station: Station, end_station: Station,
                 start_time: datetime, end_time: datetime,
                 distance_km: float):
        """
        Initialize a trip.

        Args:
            trip_id: Unique trip identifier
            user: User who took the trip
            bike: Bike used for the trip
            start_station: Starting station
            end_station: Ending station
            start_time: Trip start time
            end_time: Trip end time
            distance_km: Distance traveled in kilometers

        Raises:
            ValueError: If invalid parameters provided
        """
        super().__init__(trip_id)

        if not isinstance(user, User):
            raise ValueError("user must be a User instance")

        if not isinstance(bike, Bike):
            raise ValueError("bike must be a Bike instance")

        if not isinstance(start_station, Station):
            raise ValueError("start_station must be a Station instance")

        if not isinstance(end_station, Station):
            raise ValueError("end_station must be a Station instance")

        if not isinstance(start_time, datetime):
            raise ValueError("start_time must be a datetime object")

        if not isinstance(end_time, datetime):
            raise ValueError("end_time must be a datetime object")

        if end_time <= start_time:
            raise ValueError("end_time must be after start_time")

        if distance_km <= 0:
            raise ValueError("distance_km must be positive")

        self._user = user
        self._bike = bike
        self._start_station = start_station
        self._end_station = end_station
        self._start_time = start_time
        self._end_time = end_time
        self._distance_km = distance_km

    @property
    def trip_id(self) -> str:
        """Get trip ID."""
        return self.id

    @property
    def user(self) -> User:
        """Get user."""
        return self._user

    @property
    def bike(self) -> Bike:
        """Get bike."""
        return self._bike

    @property
    def start_station(self) -> Station:
        """Get start station."""
        return self._start_station

    @property
    def end_station(self) -> Station:
        """Get end station."""
        return self._end_station

    @property
    def start_time(self) -> datetime:
        """Get start time."""
        return self._start_time

    @property
    def end_time(self) -> datetime:
        """Get end time."""
        return self._end_time

    @property
    def distance_km(self) -> float:
        """Get distance in kilometers."""
        return self._distance_km

    @property
    def duration_minutes(self) -> float:
        """Calculate trip duration in minutes."""
        duration = self._end_time - self._start_time
        return duration.total_seconds() / 60

    def __str__(self) -> str:
        return (f"Trip {self.id}: {self.user.name} rode {self.distance_km}km "
                f"from {self.start_station.name} to {self.end_station.name}")

    def __repr__(self) -> str:
        return (f"Trip(id={self.id!r}, user={self.user.id!r}, "
                f"bike={self.bike.id!r}, duration={self.duration_minutes:.1f}min)")


class MaintenanceRecord(Entity):
    """Represents a bike maintenance record."""

    VALID_TYPES = {
        "tire_repair", "brake_adjustment", "battery_replacement",
        "chain_lubrication", "general_inspection"
    }

    def __init__(self, record_id: str, bike: Bike, date: datetime,
                 maintenance_type: str, cost: float, description: str = ""):
        """
        Initialize a maintenance record.

        Args:
            record_id: Unique record identifier
            bike: Bike being maintained
            date: Date of maintenance
            maintenance_type: Type of maintenance performed
            cost: Cost of maintenance
            description: Optional description

        Raises:
            ValueError: If invalid parameters provided
        """
        super().__init__(record_id)

        if not isinstance(bike, Bike):
            raise ValueError("bike must be a Bike instance")

        if not isinstance(date, datetime):
            raise ValueError("date must be a datetime object")

        if maintenance_type not in self.VALID_TYPES:
            raise ValueError(
                f"Maintenance type must be one of {self.VALID_TYPES}")

        if cost < 0:
            raise ValueError("Cost cannot be negative")

        self._bike = bike
        self._date = date
        self._maintenance_type = maintenance_type
        self._cost = cost
        self._description = description

    @property
    def record_id(self) -> str:
        """Get record ID."""
        return self.id

    @property
    def bike(self) -> Bike:
        """Get bike."""
        return self._bike

    @property
    def date(self) -> datetime:
        """Get maintenance date."""
        return self._date

    @property
    def maintenance_type(self) -> str:
        """Get maintenance type."""
        return self._maintenance_type

    @property
    def cost(self) -> float:
        """Get maintenance cost."""
        return self._cost

    @property
    def description(self) -> str:
        """Get description."""
        return self._description

    def __str__(self) -> str:
        return (f"Maintenance on {self.bike.id}: {self.maintenance_type} "
                f"(${self.cost:.2f})")

    def __repr__(self) -> str:
        return (f"MaintenanceRecord(id={self.id!r}, "
                f"bike={self.bike.id!r}, type={self.maintenance_type!r}, "
                f"cost=${self.cost:.2f})")
