from getpass import getpass


class Account:
    def __init__(self):
        self.balance = 0
        self.withdrawls = 0
        self.deposits = 0

    def withdraw(self, amount):
        if amount < 0:
            print("Can't withdraw negative monies.")
            return
        withdrawn = self.balance - amount
        if withdrawn < 0:
            print("Negative Compadre.")
        else:
            self.balance = withdrawn
            self.withdrawls += 1

    def deposit(self, amount):
        if amount < 0:
            print("Can't deposit negative monies.")
            return
        self.balance += amount
        self.deposits += 1

class Customer:
    unique_id = 1000

    def __init__(self, first_name, last_name, username):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = self.get_password()
        self.id = Customer.unique_id
        Customer.unique_id += 1

    def get_password(self):
        pw_prompt = "Please enter a password.\n>"
        pw_confirm = "Please confirm your password.\n>"
        while True:
            first_attempt = hash(getpass(pw_prompt))
            confirmation = hash(getpass(pw_confirm))
            if first_attempt is None or confirmation is None:
                print("Password cannot be empty.")
            elif first_attempt == confirmation:
                return confirmation
