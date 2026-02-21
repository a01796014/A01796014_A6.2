"""
Domain models for Hotel Reservation System.
"""

from dataclasses import dataclass, asdict


@dataclass
class Hotel:
    """Represents a hotel entity."""
    hotel_id: str
    name: str
    location: str
    total_rooms: int
    available_rooms: int

    def to_dict(self):
        """Convert object to dictionary."""
        return asdict(self)


@dataclass
class Customer:
    """Represents a customer entity."""
    customer_id: str
    name: str
    email: str

    def to_dict(self):
        """Convert object to dictionary."""
        return asdict(self)


@dataclass
class Reservation:
    """Represents a reservation entity."""
    reservation_id: str
    customer_id: str
    hotel_id: str

    def to_dict(self):
        """Convert object to dictionary."""
        return asdict(self)
