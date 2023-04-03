
def add(a: int,b:int):
    return a+b


class BankAccount():

    def __init__(self, starting_balance=0) -> None:
        self.bal = starting_balance

    def deposit(self, amount):
        self.bal += amount

    def withdraw(self, amount):
        self.bal -= amount

    def interest(self):
        self.bal *= 1.1
