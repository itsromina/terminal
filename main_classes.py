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