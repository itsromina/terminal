import uuid
from datetime import datetime, timedelta
from typing import List, Dict


class Wallet:
    def __init__(self, balance: float = 0.0):
        self._balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("the value must be positive")
        self._balance += amount
        return self._balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("the value must be positive")
        if amount > self._balance:
            raise ValueError("the balance is not enough")
        self._balance -= amount
        return self._balance

    def see_balance(self):
        return self._balance


class User:
    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self._password = hash(password)

    def check_password(self, password: str) -> bool:
        return self._password == hash(password)


class Passenger(User):
    def __init__(self, username: str, email: str, password: str):
        super().__init__(username, email, password)
        self.history: List['Booking'] = []
        self.wallet = Wallet()

    def view_history(self):
        return self.history

    def charge_wallet(self, amount):
        return self.wallet.deposit(amount)

    def change_password(self, old_pass: str, new_pass: str):
        if not self.check_password(old_pass):
            raise ValueError("the old password was wrong")
        self._password = hash(new_pass)


class Admin(User):
    def __init__(self, username: str, email: str, password: str):
        super().__init__(username, email, password)

    def check_total_money_of_each_trip(self):
        ...

    def check_the_total_money_of_terminal(self):
        ...


class Trip:
    def __init__(self, trip_id: str, mode: str, from_city: str, to_city: str, departure_time: str,
                 price_per_seat: float, available_seats: int = 50):
        self.trip_id = trip_id
        self.mode = mode
        self.from_city = from_city
        self.to_city = to_city
        self.departure_time = datetime.strptime(departure_time, "%Y-%m-%d %H:%M")
        self.price_per_seat = price_per_seat
        self.available_seats = available_seats
        self.bookings: List['Booking'] = []
        self.seats: Dict[int, bool] = {i: True for i in range(1, available_seats + 1)}  # true means available seat

    def is_available(self, seat_count: int) -> bool:
        return sum(self.seats.values()) >= seat_count  # t=1/f=0

    def book_seats(self, seats: List[int]) -> bool:
        for seat in seats:
            if not self.seats.get(seat, False):
                return False
        for seat in seats:
            self.seats[seat] = False
        self.available_seats -= len(seats)
        return True

    def cancel_seats(self, seats: List[int]):
        for seat in seats:
            self.seats[seat] = True
        self.available_seats += len(seats)


class Flight(Trip):
    def __init__(self, trip_id: str, from_city: str, to_city: str, departure_time: str, price_per_seat: float,
                 airline: str = "mahan"):
        super().__init__(trip_id, "airplane", from_city, to_city, departure_time, price_per_seat)
        self.airline = airline


class BusTrip(Trip):
    def __init__(self, trip_id: str, from_city: str, to_city: str, departure_time: str, price_per_seat: float,
                 bus_company: str = "idk"):
        super().__init__(trip_id, "bus", from_city, to_city, departure_time, price_per_seat)
        self.bus_company = bus_company


class TrainTrip(Trip):
    def __init__(self, trip_id: str, from_city: str, to_city: str, departure_time: str, price_per_seat: float,
                 train_number: str = "R999"):
        super().__init__(trip_id, "subway", from_city, to_city, departure_time, price_per_seat)
        self.train_number = train_number

class Booking: #????
    def __init__(self, booking_id: str, passenger: Passenger, trip: Trip, seats: List[int], total_price: float, passenger_types: Dict[str, int]={"adult":1}):
        self.booking_id = booking_id
        self.passenger = passenger
        self.trip = trip
        self.seats = seats
        self.passenger_types = passenger_types
        self.total_price = total_price
        self.status = "confirmed"
        self.booking_time = datetime.now()

    def calculate_price(self, base_price: float) -> float:
        price = 0
        price += self.passenger_types.get('adult', 0) * base_price
        price += self.passenger_types.get('child', 0) * base_price * 0.5
        price += self.passenger_types.get('baby', 0) * base_price * 0.1
        return price

    def can_cancel(self, current_time: datetime) -> tuple[bool, str]:
        if self.status != "confirmed":
            return False, "it has been canceled already"
        time_to_departure = self.trip.departure_time - current_time
        if time_to_departure < timedelta(hours=24):
            return False, "u can cancel only 24 hrs before departure"
        return True, "acceptable canceling"

    def cancel(self, system: 'TravelSystem', current_time: datetime) -> tuple[bool, str]:
        can, msg = self.can_cancel(current_time)
        if not can:
            return False, msg
        self.trip.cancel_seats(self.seats)
        self.status = "cancelled"
        refund = self.total_price * 0.8
        self.passenger.wallet.deposit(refund)
        self.passenger.history.remove(self) if self in self.passenger.history else None
        system.bookings.remove(self)
        return True, f"your reserved has been canceled and {refund}$ deposited to your wallet"
