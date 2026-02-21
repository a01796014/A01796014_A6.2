"""
Unit tests for Hotel Reservation System.
"""

import os
import unittest
from services import (
    HotelService,
    CustomerService,
    ReservationService
)
from storage import load_data


DATA_FILES = [
    "data/hotels.json",
    "data/customers.json",
    "data/reservations.json"
]


class TestHotelSystem(unittest.TestCase):
    """Unit tests for Hotel Reservation System."""

    def setUp(self):
        """Initialize empty data files before each test."""
        os.makedirs("data", exist_ok=True)
        for file in DATA_FILES:
            with open(file, "w", encoding="utf-8") as f:
                f.write("[]")

    def test_create_hotel(self):
        """Test creating a hotel."""
        hotel = HotelService.create_hotel(
            "Test Hotel", "NYC", 10
        )
        self.assertEqual(hotel.total_rooms, 10)

    def test_create_customer(self):
        """Test creating a customer."""
        customer = CustomerService.create_customer(
            "John", "john@test.com"
        )
        self.assertEqual(customer.name, "John")

    def test_create_reservation(self):
        """Test creating a reservation."""
        hotel = HotelService.create_hotel(
            "Test Hotel", "NYC", 1
        )
        customer = CustomerService.create_customer(
            "Jane", "jane@test.com"
        )

        reservation = ReservationService.create_reservation(
            customer.customer_id,
            hotel.hotel_id
        )

        self.assertIsNotNone(reservation.reservation_id)

    def test_cancel_reservation(self):
        """Test cancelling an existing reservation."""
        hotel = HotelService.create_hotel(
            "Hotel A", "LA", 1
        )
        customer = CustomerService.create_customer(
            "Ana", "ana@test.com"
        )

        reservation = ReservationService.create_reservation(
            customer.customer_id,
            hotel.hotel_id
        )

        ReservationService.cancel_reservation(
            reservation.reservation_id
        )

        reservations = load_data("data/reservations.json")
        self.assertEqual(len(reservations), 0)

    def test_modify_and_delete_hotel(self):
        """Test modifying and deleting a hotel."""
        hotel = HotelService.create_hotel(
            "Hotel B", "TX", 5
        )

        HotelService.modify_hotel(
            hotel.hotel_id,
            name="Modified Hotel"
        )

        hotels = HotelService.display_hotels()
        self.assertEqual(hotels[0]["name"], "Modified Hotel")

        HotelService.delete_hotel(hotel.hotel_id)
        hotels = HotelService.display_hotels()
        self.assertEqual(len(hotels), 0)

    def test_modify_and_delete_customer(self):
        """Test modifying and deleting a customer."""
        customer = CustomerService.create_customer(
            "Mark", "mark@test.com"
        )

        CustomerService.modify_customer(
            customer.customer_id,
            name="Mark Updated"
        )

        customers = CustomerService.display_customers()
        self.assertEqual(customers[0]["name"], "Mark Updated")

        CustomerService.delete_customer(customer.customer_id)
        customers = CustomerService.display_customers()
        self.assertEqual(len(customers), 0)

    def test_no_rooms_available(self):
        """Test reservation fails when no rooms are available."""
        hotel = HotelService.create_hotel(
            "Small Hotel", "CA", 1
        )
        customer1 = CustomerService.create_customer(
            "A", "a@test.com"
        )
        customer2 = CustomerService.create_customer(
            "B", "b@test.com"
        )

        ReservationService.create_reservation(
            customer1.customer_id,
            hotel.hotel_id
        )

        with self.assertRaises(ValueError):
            ReservationService.create_reservation(
                customer2.customer_id,
                hotel.hotel_id
            )

    def test_cancel_non_existing_reservation(self):
        """Test cancelling a reservation that does not exist."""
        ReservationService.cancel_reservation("fake-id")
        reservations = load_data("data/reservations.json")
        self.assertEqual(reservations, [])

    def test_invalid_json_handling(self):
        """Test system behavior when JSON file contains invalid data."""
        with open("data/hotels.json", "w", encoding="utf-8") as file:
            file.write("INVALID_JSON")

        hotels = HotelService.display_hotels()
        self.assertEqual(hotels, [])


if __name__ == "__main__":
    unittest.main()
