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
