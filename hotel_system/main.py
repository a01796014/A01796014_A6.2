"""
Simple CLI runner for Hotel Reservation System.
"""

from services import (
    HotelService,
    CustomerService,
    ReservationService
)


def main():
    """Run simple demo operations."""

    print("\n--- Hotels ---")
    hotels = HotelService.display_hotels()
    for hotel in hotels:
        print(hotel)

    print("\n--- Customers ---")
    customers = CustomerService.display_customers()
    for customer in customers:
        print(customer)

    print("\n--- Creating New Reservation ---")
    reservation = ReservationService.create_reservation(
        "c1",
        "h2"
    )
    print("Created reservation:", reservation.to_dict())

    print("\n--- Updated Hotels ---")
    hotels = HotelService.display_hotels()
    for hotel in hotels:
        print(hotel)


if __name__ == "__main__":
    main()
