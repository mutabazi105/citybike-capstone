"""
Unit tests for CityBike models module.
Tests domain models: Bike, ElectricBike, ClassicBike, Station, User, Trip, MaintenanceRecord.
"""
import pytest
from datetime import datetime, timedelta
from citybike.models import (
    Bike, ElectricBike, ClassicBike, Station, User, CasualUser, MemberUser,
    Trip, MaintenanceRecord
)
from citybike.utils import ValidationError


class TestBikeModels:
    """Test cases for Bike hierarchy."""

    def test_classic_bike_creation(self):
        """Test creating a ClassicBike instance."""
        bike = ClassicBike(bike_id=101, station_id=1)
        assert bike.bike_id == 101
        assert bike.station_id == 1
        assert bike.bike_type == "Classic"
        assert bike.is_available is True

    def test_electric_bike_creation(self):
        """Test creating an ElectricBike with battery level."""
        bike = ElectricBike(bike_id=201, station_id=2, battery_level=85)
        assert bike.bike_id == 201
        assert bike.battery_level == 85
        assert bike.bike_type == "Electric"

    def test_bike_availability_toggle(self):
        """Test toggling bike availability."""
        bike = ClassicBike(bike_id=102, station_id=1)
        assert bike.is_available is True
        bike.is_available = False
        assert bike.is_available is False

    def test_invalid_bike_id(self):
        """Test that invalid bike_id raises error."""
        with pytest.raises(ValidationError):
            ClassicBike(bike_id=-1, station_id=1)

    def test_invalid_battery_level(self):
        """Test that invalid battery level raises error."""
        with pytest.raises(ValidationError):
            ElectricBike(bike_id=201, station_id=2, battery_level=150)


class TestStationModel:
    """Test cases for Station model."""

    def test_station_creation(self):
        """Test creating a Station instance."""
        station = Station(
            station_id=1,
            name="Central Station",
            latitude=52.5200,
            longitude=13.4050,
            capacity=20
        )
        assert station.station_id == 1
        assert station.name == "Central Station"
        assert station.capacity == 20

    def test_invalid_coordinates(self):
        """Test that invalid coordinates raise error."""
        with pytest.raises(ValidationError):
            Station(
                station_id=1,
                name="Invalid",
                latitude=91.0,  # Invalid latitude
                longitude=13.4050,
                capacity=20
            )

    def test_invalid_capacity(self):
        """Test that negative capacity raises error."""
        with pytest.raises(ValidationError):
            Station(
                station_id=1,
                name="Invalid",
                latitude=52.5200,
                longitude=13.4050,
                capacity=-5
            )


class TestUserModels:
    """Test cases for User hierarchy."""

    def test_casual_user_creation(self):
        """Test creating a CasualUser."""
        user = CasualUser(user_id=1001, name="John Doe",
                          email="john@example.com")
        assert user.user_id == 1001
        assert user.name == "John Doe"
        assert user.user_type == "Casual"

    def test_member_user_creation(self):
        """Test creating a MemberUser."""
        user = MemberUser(user_id=2001, name="Jane Doe",
                          email="jane@example.com")
        assert user.user_id == 2001
        assert user.user_type == "Member"

    def test_invalid_user_email(self):
        """Test that invalid email raises error."""
        with pytest.raises(ValidationError):
            CasualUser(user_id=1001, name="John", email="invalid-email")

    def test_invalid_user_id(self):
        """Test that invalid user_id raises error."""
        with pytest.raises(ValidationError):
            CasualUser(user_id=-1, name="John", email="john@example.com")


class TestTripModel:
    """Test cases for Trip model."""

    def test_trip_creation(self):
        """Test creating a Trip."""
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=30)

        trip = Trip(
            trip_id=5001,
            user_id=1001,
            bike_id=101,
            start_station_id=1,
            end_station_id=2,
            start_time=start_time,
            end_time=end_time,
            distance=5.2,
            status="Completed"
        )
        assert trip.trip_id == 5001
        assert trip.distance == 5.2
        assert trip.status == "Completed"

    def test_trip_duration_calculation(self):
        """Test that trip duration is calculated correctly."""
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=45)

        trip = Trip(
            trip_id=5001,
            user_id=1001,
            bike_id=101,
            start_station_id=1,
            end_station_id=2,
            start_time=start_time,
            end_time=end_time,
            distance=5.2,
            status="Completed"
        )
        assert trip.duration_minutes == 45

    def test_invalid_distance(self):
        """Test that negative distance raises error."""
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=30)

        with pytest.raises(ValidationError):
            Trip(
                trip_id=5001,
                user_id=1001,
                bike_id=101,
                start_station_id=1,
                end_station_id=2,
                start_time=start_time,
                end_time=end_time,
                distance=-5.0,
                status="Completed"
            )


class TestMaintenanceRecordModel:
    """Test cases for MaintenanceRecord model."""

    def test_maintenance_record_creation(self):
        """Test creating a MaintenanceRecord."""
        maintenance_date = datetime.now()
        record = MaintenanceRecord(
            maintenance_id=3001,
            bike_id=101,
            maintenance_type="Repair",
            cost=50.0,
            maintenance_date=maintenance_date,
            description="Chain replacement"
        )
        assert record.maintenance_id == 3001
        assert record.maintenance_type == "Repair"
        assert record.cost == 50.0

    def test_invalid_maintenance_cost(self):
        """Test that negative cost raises error."""
        with pytest.raises(ValidationError):
            MaintenanceRecord(
                maintenance_id=3001,
                bike_id=101,
                maintenance_type="Repair",
                cost=-50.0,
                maintenance_date=datetime.now(),
                description="Chain replacement"
            )

    def test_invalid_maintenance_type(self):
        """Test that invalid maintenance type raises error."""
        with pytest.raises(ValidationError):
            MaintenanceRecord(
                maintenance_id=3001,
                bike_id=101,
                maintenance_type="InvalidType",
                cost=50.0,
                maintenance_date=datetime.now(),
                description="Description"
            )
