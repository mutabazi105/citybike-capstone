"""
Pricing strategies for bike-sharing system.
Implements the Strategy Pattern for flexible pricing calculations.
"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional


class PricingStrategy(ABC):
    """Abstract base class for pricing strategies."""

    @abstractmethod
    def calculate_fare(self, duration_minutes: float,
                      distance_km: float,
                      bike_type: str = "classic",
                      time_of_day: Optional[datetime] = None) -> float:
        """
        Calculate fare for a trip.
        
        Args:
            duration_minutes: Trip duration in minutes
            distance_km: Trip distance in kilometers
            bike_type: Type of bike ("classic" or "electric")
            time_of_day: Trip start time for time-based pricing
            
        Returns:
            Calculated fare in currency units
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Get strategy name."""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """Get strategy description."""
        pass


class CasualPricingStrategy(PricingStrategy):
    """
    Pay-per-minute pricing for casual users.
    No membership, higher base rates.
    """

    # Base rate: €0.30 per minute
    BASE_RATE_PER_MINUTE = 0.30
    # Minimum fare
    MINIMUM_FARE = 2.00
    # Electric bike surcharge: 20%
    ELECTRIC_SURCHARGE = 0.20

    def calculate_fare(self, duration_minutes: float,
                      distance_km: float,
                      bike_type: str = "classic",
                      time_of_day: Optional[datetime] = None) -> float:
        """Calculate fare for casual user."""
        # Base calculation: minutes * rate
        fare = duration_minutes * self.BASE_RATE_PER_MINUTE

        # Apply electric bike surcharge
        if bike_type == "electric":
            fare *= (1 + self.ELECTRIC_SURCHARGE)

        # Apply minimum fare
        fare = max(fare, self.MINIMUM_FARE)

        return round(fare, 2)

    def get_name(self) -> str:
        return "Casual (Pay-Per-Minute)"

    def get_description(self) -> str:
        return f"€{self.BASE_RATE_PER_MINUTE}/min (min €{self.MINIMUM_FARE})"


class MemberPricingStrategy(PricingStrategy):
    """
    Discounted pricing for members.
    Includes unlimited trips up to max duration.
    """

    # Base rate: €0.18 per minute (40% discount from casual)
    BASE_RATE_PER_MINUTE = 0.18
    # Unlimited rides up to 45 minutes
    UNLIMITED_DURATION = 45
    # Minimum fare
    MINIMUM_FARE = 1.00
    # Electric bike surcharge: 10%
    ELECTRIC_SURCHARGE = 0.10

    def calculate_fare(self, duration_minutes: float,
                      distance_km: float,
                      bike_type: str = "classic",
                      time_of_day: Optional[datetime] = None) -> float:
        """Calculate fare for member."""
        # Free rides up to 45 minutes
        if duration_minutes <= self.UNLIMITED_DURATION:
            return 0.00

        # Charge for excess time
        excess_minutes = duration_minutes - self.UNLIMITED_DURATION
        fare = excess_minutes * self.BASE_RATE_PER_MINUTE

        # Apply electric bike surcharge
        if bike_type == "electric":
            fare *= (1 + self.ELECTRIC_SURCHARGE)

        # Apply minimum if trip was very short
        fare = max(fare, self.MINIMUM_FARE) if duration_minutes > 0 else 0

        return round(fare, 2)

    def get_name(self) -> str:
        return "Member (First 45min Free)"

    def get_description(self) -> str:
        return f"Free 45min, then €{self.BASE_RATE_PER_MINUTE}/min"


class PeakHourPricingStrategy(PricingStrategy):
    """
    Dynamic pricing based on time of day.
    Higher rates during peak hours (8-9am, 5-7pm).
    """

    # Peak hours: 8-9 and 17-19 (rush hour)
    PEAK_HOURS = [8, 17, 18]
    PEAK_MULTIPLIER = 1.5  # 50% more

    # Off-peak base rate
    BASE_RATE_PER_MINUTE = 0.25
    MINIMUM_FARE = 1.50

    def calculate_fare(self, duration_minutes: float,
                      distance_km: float,
                      bike_type: str = "classic",
                      time_of_day: Optional[datetime] = None) -> float:
        """Calculate fare with peak-hour multiplier."""
        if time_of_day is None:
            time_of_day = datetime.now()

        # Base calculation
        fare = duration_minutes * self.BASE_RATE_PER_MINUTE

        # Apply peak hour multiplier
        if time_of_day.hour in self.PEAK_HOURS:
            fare *= self.PEAK_MULTIPLIER

        # Apply electric bike surcharge
        if bike_type == "electric":
            fare *= 1.15

        # Apply minimum
        fare = max(fare, self.MINIMUM_FARE)

        return round(fare, 2)

    def get_name(self) -> str:
        return "Peak-Hour Dynamic Pricing"

    def get_description(self) -> str:
        return f"€{self.BASE_RATE_PER_MINUTE}/min (x{self.PEAK_MULTIPLIER} during 8-9am, 5-7pm)"


class DistanceBasedPricingStrategy(PricingStrategy):
    """
    Pricing based on distance traveled.
    Better for longer trips.
    """

    # €0.80 per km
    RATE_PER_KM = 0.80
    # Minimum fare for short trips
    MINIMUM_FARE = 2.50
    # Time-based fallback: €0.15/min
    FALLBACK_RATE_PER_MINUTE = 0.15

    def calculate_fare(self, duration_minutes: float,
                      distance_km: float,
                      bike_type: str = "classic",
                      time_of_day: Optional[datetime] = None) -> float:
        """Calculate fare based on distance."""
        if distance_km <= 0:
            # Fallback to time-based
            fare = duration_minutes * self.FALLBACK_RATE_PER_MINUTE
        else:
            fare = distance_km * self.RATE_PER_KM

        # Apply electric bike surcharge
        if bike_type == "electric":
            fare *= 1.25

        # Apply minimum
        fare = max(fare, self.MINIMUM_FARE)

        return round(fare, 2)

    def get_name(self) -> str:
        return "Distance-Based Pricing"

    def get_description(self) -> str:
        return f"€{self.RATE_PER_KM}/km (min €{self.MINIMUM_FARE})"


class PricingFactory:
    """Factory for creating pricing strategies."""

    STRATEGIES = {
        "casual": CasualPricingStrategy,
        "member": MemberPricingStrategy,
        "peak_hour": PeakHourPricingStrategy,
        "distance": DistanceBasedPricingStrategy,
    }

    @staticmethod
    def create_strategy(strategy_name: str) -> PricingStrategy:
        """
        Create a pricing strategy by name.
        
        Args:
            strategy_name: Name of strategy
            
        Returns:
            PricingStrategy instance
            
        Raises:
            ValueError: If strategy not found
        """
        strategy_class = PricingFactory.STRATEGIES.get(
            strategy_name.lower()
        )

        if not strategy_class:
            available = ", ".join(PricingFactory.STRATEGIES.keys())
            raise ValueError(
                f"Unknown strategy '{strategy_name}'. "
                f"Available: {available}"
            )

        return strategy_class()

    @staticmethod
    def list_available() -> dict:
        """List all available strategies with descriptions."""
        strategies = {}
        for name, strategy_class in PricingFactory.STRATEGIES.items():
            instance = strategy_class()
            strategies[name] = {
                "name": instance.get_name(),
                "description": instance.get_description(),
            }
        return strategies


class TripFareCalculator:
    """Calculates fare using a given pricing strategy."""

    def __init__(self, strategy: PricingStrategy):
        """
        Initialize with a pricing strategy.
        
        Args:
            strategy: PricingStrategy instance
        """
        self.strategy = strategy

    def calculate(self, duration_minutes: float,
                  distance_km: float,
                  bike_type: str = "classic",
                  time_of_day: Optional[datetime] = None) -> dict:
        """
        Calculate trip fare and return detailed breakdown.
        
        Returns:
            Dictionary with fare and metadata
        """
        fare = self.strategy.calculate_fare(
            duration_minutes, distance_km, bike_type, time_of_day
        )

        return {
            "fare": fare,
            "strategy": self.strategy.get_name(),
            "duration_minutes": duration_minutes,
            "distance_km": distance_km,
            "bike_type": bike_type,
            "currency": "€",
        }

    def set_strategy(self, strategy: PricingStrategy):
        """Change pricing strategy."""
        self.strategy = strategy
