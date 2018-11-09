from getpass import getpass
import hashlib


class Account:
    '''Base Account class from which Savings, Checkings, and 401k
    Accounts will be structured from'''
    def __init__(self, account_num):
        '''Takes the account_num from the respective sub class
        and uses it when creating an account'''
        self.account_id = account_num
        self.balance = 0
        self.withdraws = 0
        self.deposits = 0
        self.interest = 0

    def withdraw(self, amount):
        '''Takes the amount of money to withdraw and will
        make the new balance reflect that change'''
        if amount < 0:
            print("Can't withdraw negative monies.")
            return
        withdrawn = self.balance - amount
        if withdrawn < 0:
            print("You will incur over draft fees of 35$.")
            withdrawn -= 35
            self.balance = withdrawn
        else:
            self.balance = withdrawn
            self.withdraws += 1

    def deposit(self, amount):
        '''Takes the amount of money to deposit and will
        make the new balance reflect that change'''
        if amount < 0:
            print("Can't deposit negative monies.")
            return
        self.balance += amount
        self.deposits += 1

    def __str__(self, type_of_account):
        '''Takes the type of account and returns
        the proper string representation for an account'''
        acc_string = "{0} account: {1} \n   Balance: ${2:.2f}\n   " \
                     "Interest: {3}%\n   Withdraws: {4}\n   " \
                     "Deposits: {5}".format(
                        type_of_account, self.account_id,
                        self.balance, float(self.interest) * 100,
                        self.withdraws, self.deposits)
        return acc_string


class Checking(Account):
    '''Subclass for Checking account.'''
    checking_id = 10000000

    def __init__(self):
        '''Creates unique id'd checking account'''
        super().__init__(Checking.checking_id)
        print("Checking", Checking.checking_id)
        Checking.checking_id += 1

    def __str__(self):
        '''Sends Account.__str__ the Checking string for printing'''
        return super().__str__("Checking")


class Savings(Account):
    '''Subclass for Savings account.'''
    savings_id = 10000000

    def __init__(self):
        '''Creates unique id'd savings account'''
        super().__init__(Savings.savings_id)
        print("Savings", Savings.savings_id)
        Savings.savings_id += 1
        self.interest = 0.05

    def __str__(self):
        '''Sends Account.__str__ the Savings string for printing'''
        return super().__str__("Savings")


class FourOhOneK(Account):
    '''Subclass for 401k account.'''
    four_oh_one_k_id = 10000000

    def __init__(self):
        '''Creates unique id'd 401k account'''
        super().__init__(FourOhOneK.four_oh_one_k_id)
        FourOhOneK.four_oh_one_k_id += 1
        self.interest = 0.05

    def __str__(self):
        '''Sends Account.__str__ the 401k string for printing'''
        return super().__str__("401k")


class Customer:
    '''Class used to represent a customer'''
    customer_id = 1000
    '''Customers is a dictionary of Customer(), keys are usernames
    and values are the Customer() objects themselves'''
    customers = dict()

    def __init__(self, first_name, last_name, username, age):
        '''Takes first_name, last_name, username, and age and will
        prompt the user for passwords that are stored as md5 sum hashes.'''
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.age = age
        self.id = Customer.customer_id
        self.accounts = {'Checking': {}, 'Savings': {}, '401k': {}}
        if username in Customer.customers:
            print("Username taken.")
            return None
        self.password = self.get_password()
        Customer.customers.update({username: self})
        Customer.customer_id += 1

    def get_password(self):
        '''Instance method that will prompt the user for a password'''
        pw_prompt = "Please enter a password.\n>"
        pw_confirm = "Please confirm your password.\n>"
        while True:
            try:
                first_attempt = getpass(pw_prompt)
                confirmation = getpass(pw_confirm)
                if not first_attempt or not confirmation:
                    print("Password cannot be empty.")
                elif first_attempt == confirmation:
                    digest = hashlib.md5(
                            confirmation.encode("utf-8")).hexdigest()
                    return digest
                else:
                    print("Passwords do not match. Try Again.")
            except (KeyboardInterrupt, EOFError):
                # Passing silently to not allow account without password
                pass

    def __str__(self):
        '''String representation of a Customer()'''
        output = "Name: {} {}\nAge: {}\nId: {}\nUsername: {}"
        return output.format(
                self.first_name, self.last_name,
                self.age, self.id, self.username)
