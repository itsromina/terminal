import uuid
from datetime import datetime,timedelta
from typing import List,Dict

class Wallet:
    def __init__(self,balance:float=0.0):
        self._balance=balance
    def deposit(self,amount):
        if amount<=0:
            raise ValueError("the value must be positive")
        self._balance+=amount
        return self._balance
    def withdraw(self,amount):
        if amount<=0:
            raise ValueError("the value must be positive")
        if amount>self._balance:
            raise ValueError("the balance is not enough")
        self._balance-=amount
        return self._balance
    def see_balance(self):
        return self._balance
