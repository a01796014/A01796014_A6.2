"""
Business logic for Hotel Reservation System.
"""

import uuid
from models import Hotel, Customer, Reservation
from storage import load_data, save_data


HOTELS_FILE = "data/hotels.json"
CUSTOMERS_FILE = "data/customers.json"
RESERVATIONS_FILE = "data/reservations.json"


class HotelService:
    """Service class responsible for hotel operations."""

    @staticmethod
    def create_hotel(name, location, total_rooms):
        """Create and persist a new hotel."""
        hotels = load_data(HOTELS_FILE)
        hotel_id = str(uuid.uuid4())
        hotel = Hotel(
            hotel_id, name, location, total_rooms, total_rooms
        )
        hotels.append(hotel.to_dict())
        save_data(HOTELS_FILE, hotels)
        return hotel

    @staticmethod
    def delete_hotel(hotel_id):
        """Delete a hotel by its ID."""
        hotels = load_data(HOTELS_FILE)
        hotels = [
            hotel for hotel in hotels
            if hotel["hotel_id"] != hotel_id
        ]
        save_data(HOTELS_FILE, hotels)

    @staticmethod
    def modify_hotel(hotel_id, **kwargs):
        """Modify existing hotel attributes."""
        hotels = load_data(HOTELS_FILE)
        for hotel in hotels:
            if hotel["hotel_id"] == hotel_id:
                hotel.update(kwargs)
        save_data(HOTELS_FILE, hotels)

    @staticmethod
    def display_hotels():
        """Return list of all hotels."""
        return load_data(HOTELS_FILE)

    @staticmethod
    def reserve_room(hotel_id):
        """Reserve a room in a hotel."""
        hotels = load_data(HOTELS_FILE)
        for hotel in hotels:
            if hotel["hotel_id"] == hotel_id:
                if hotel["available_rooms"] > 0:
                    hotel["available_rooms"] -= 1
                else:
                    raise ValueError("No rooms available")
        save_data(HOTELS_FILE, hotels)

    @staticmethod
    def cancel_reservation_room(hotel_id):
        """Increase available rooms after reservation cancellation."""
        hotels = load_data(HOTELS_FILE)
        for hotel in hotels:
            if hotel["hotel_id"] == hotel_id:
                hotel["available_rooms"] += 1
        save_data(HOTELS_FILE, hotels)


class CustomerService:
    """Service class responsible for customer operations."""

    @staticmethod
    def create_customer(name, email):
        """Create and persist a new customer."""
        customers = load_data(CUSTOMERS_FILE)
        customer_id = str(uuid.uuid4())
        customer = Customer(customer_id, name, email)
        customers.append(customer.to_dict())
        save_data(CUSTOMERS_FILE, customers)
        return customer

    @staticmethod
    def delete_customer(customer_id):
        """Delete a customer by ID."""
        customers = load_data(CUSTOMERS_FILE)
        customers = [
            cust for cust in customers
            if cust["customer_id"] != customer_id
        ]
        save_data(CUSTOMERS_FILE, customers)

    @staticmethod
    def modify_customer(customer_id, **kwargs):
        """Modify existing customer attributes."""
        customers = load_data(CUSTOMERS_FILE)
        for cust in customers:
            if cust["customer_id"] == customer_id:
                cust.update(kwargs)
        save_data(CUSTOMERS_FILE, customers)

    @staticmethod
    def display_customers():
        """Return list of all customers."""
        return load_data(CUSTOMERS_FILE)


class ReservationService:
    """Service class responsible for reservation operations."""

    @staticmethod
    def create_reservation(customer_id, hotel_id):
        """Create a reservation for a customer in a hotel."""
        reservations = load_data(RESERVATIONS_FILE)
        reservation_id = str(uuid.uuid4())

        reservation = Reservation(
            reservation_id,
            customer_id,
            hotel_id
        )

        HotelService.reserve_room(hotel_id)

        reservations.append(reservation.to_dict())
        save_data(RESERVATIONS_FILE, reservations)
        return reservation

    @staticmethod
    def cancel_reservation(reservation_id):
        """Cancel a reservation by its ID."""
        reservations = load_data(RESERVATIONS_FILE)

        for reservation in reservations:
            if reservation["reservation_id"] == reservation_id:
                HotelService.cancel_reservation_room(
                    reservation["hotel_id"]
                )

        reservations = [
            res for res in reservations
            if res["reservation_id"] != reservation_id
        ]

        save_data(RESERVATIONS_FILE, reservations)
