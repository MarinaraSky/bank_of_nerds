#! /usr/bin/env python3
import bon_Classes as bon
from getpass import getpass
import hashlib
import pickle
import os


# Global stirng used to reset terminal
clear_screen = "\033c"


def main():
    '''Main driver for bank of nerds'''
    startup()
    print(clear_screen)
    main_loop = True
    while main_loop:
        main_loop = menu_loop()
    shutdown()


def menu_loop():
    '''Main menu loop that will return True if user wants to
    interact with another customer and False to exit'''
    loop = True
    while loop:
        login_options = {'1': user_login, '2': new_customer,
                         '3': list_users, 'Q': None}
        login_menu = "1) Existing Customer.\n2) New User.\n" \
                     "3) List Users\nQ) Quit.\n>"
        try:
            selection = login_options[my_input(login_menu).upper()]
            if selection is None:
                shutdown()
                return
            loop = selection()
            # Used to end loop if customer is found
            if isinstance(loop, bon.Customer):
                break
        except KeyError:
            print("Not a Valid option.")
    # instantiating customer for clarity
    customer = loop
    loop = True
    while loop:
        loop = account_management(customer)
        my_input("Enter to Continue.")
        print(clear_screen)
    another = "Would you like to return to the main menu(Y/N)?\n>"
    selection = my_input(another)
    # Really only care if user puts in y or Y
    if selection.upper() == "Y":
        return True
    else:
        return False


def startup():
    '''Startup function that will read the database in
    and set account and user id's, or create default
    users as required.'''
    loaded = [0, 0, 0, 0, None]
    try:
        file = open(".bon_database.jack", "rb")
        try:
            loaded = MyUnpickler(file).load()
        except pickle.UnpicklingError:
            print("Corrupted database.")
            my_input("Enter to continue.")
            raise FileNotFoundError
        file.close()
        bon.Checking.checking_id = loaded[0]
        bon.Savings.savings_id = loaded[1]
        bon.Customer.customer_id = loaded[2]
        bon.FourOhOneK.four_oh_one_k_id = loaded[3]
        bon.Customer.customers = loaded[4]
    except FileNotFoundError:  # Create Default accounts
        dave = bon.Customer("Dave", "Flanagan", "d.flan", 21)
        jack = bon.Customer("Jack", "Spence", "j.spen", 99)
        dave.accounts['Checking'].update(
                {bon.Checking.checking_id: bon.Checking()})
        dave.accounts['Savings'].update(
                {bon.Savings.savings_id: bon.Savings()})
        dave.accounts['401k'].update(
                {bon.FourOhOneK.four_oh_one_k_id: bon.FourOhOneK()})
        jack.accounts['Checking'].update(
                {bon.Checking.checking_id: bon.Checking()})
        jack.accounts['Savings'].update(
                {bon.Savings.savings_id: bon.Savings()})
        jack.accounts['401k'].update(
                {bon.FourOhOneK.four_oh_one_k_id: bon.FourOhOneK()})


def shutdown():
    '''Saves the database with the current id's for accounts and
    customers.'''
    saving = [bon.Checking.checking_id, bon.Savings.savings_id,
              bon.Customer.customer_id, bon.FourOhOneK.four_oh_one_k_id,
              bon.Customer.customers]
    with open(".bon_database.jack", "w+b") as file:
        pickle.dump(saving, file)


def list_users():
    '''Used to list users from main menu.'''
    for customer in bon.Customer.customers:
        print("Customer", bon.Customer.customers[customer])
        list_accounts(bon.Customer.customers[customer].accounts['Checking'])
        list_accounts(bon.Customer.customers[customer].accounts['Savings'])
        list_accounts(bon.Customer.customers[customer].accounts['401k'])

    my_input("Enter to Continue.")
    print(clear_screen)
    return True


def new_customer():
    '''Prompts the user for required fields to make a new user.'''
    first_name_prompt = "Please enter your first name.\n>"
    last_name_prompt = "Please enter your last name.\n>"
    username_prompt = "Please enter your desired username.\n>"
    age_prompt = "Please enter your age.\n>"

    first_name = my_input(first_name_prompt)
    last_name = my_input(last_name_prompt)
    username = my_input(username_prompt)
    try:
        age = int(my_input(age_prompt))
    except ValueError:
        print("Not a valid age.")
        return True

    new = bon.Customer(first_name, last_name, username, age)
    if new:
        # Loop Variable
        return True
    else:
        return False


def user_login():
    '''Checks in the Customer.customers dictionary for submitted username
    and will prompt for their password. Will log the user in if username and
    password match'''
    login_prompt = "Please enter your user ID.\n>"
    password_prompt = "Please enter your password.\n>"
    error_prompt = "Cannot log in.\n"
    login_attempt = my_input(login_prompt)
    try:
        if bon.Customer.customers[login_attempt].password == hashlib.md5(
                getpass(password_prompt).encode("utf-8")).hexdigest():
            print("Success")
            return bon.Customer.customers[login_attempt]
        else:
            print("Fail")
            return True
    except KeyError:
        print(error_prompt)
        return True


def account_management(selected_customer):
    '''Takes the customer object found after logging in and will prompt
    the user with the account management menu.'''
    account_prompt = "1) New Checking\n2) New Savings\n3) New 401k\n" \
                     "4) Deposit Checking\n5) Savings Deposit\n" \
                     "6) Deposit 401k\n7) Checking Withdraw\n" \
                     "8) Savings Withdraw\n9) 401k Withdraw\n" \
                     "10) List Balances\nQ) Exit\n>"
    account_input = my_input(account_prompt)
    if account_input.upper() == "Q":
        return False
    elif account_input == "1":
        selected_customer.accounts['Checking'].update(
                {bon.Checking.checking_id: bon.Checking()})
    elif account_input == "2":
        selected_customer.accounts['Savings'].update(
                {bon.Savings.savings_id: bon.Savings()})
    elif account_input == "3":
        selected_customer.accounts['401k'].update(
                {bon.FourOhOneK.four_oh_one_k_id: bon.FourOhOneK()})
    elif account_input == "4":
        account_deposit(selected_customer, 'Checking')
    elif account_input == "5":
        account_deposit(selected_customer, 'Savings')
    elif account_input == "6":
        account_deposit(selected_customer, '401k')
    elif account_input == "7":
        account_withdraw(selected_customer, 'Checking')
    elif account_input == "8":
        account_withdraw(selected_customer, 'Savings')
    elif account_input == "9":
        account_withdraw(selected_customer, '401k')
    elif account_input == "10":
        list_accounts(selected_customer.accounts['Checking'])
        list_accounts(selected_customer.accounts['Savings'])
        list_accounts(selected_customer.accounts['401k'])
    return True


def account_withdraw(customer, account_type):
    '''Takes the customer object from account management and the type of
    account to withdraw money from that account.'''
    list_accounts(customer.accounts[account_type])
    selected, amount = get_amount()
    # Check to verify user can withdraw from 401k
    if account_type == '401k' and customer.age < 67:
        print("Cannont withdraw from 401k until 67 years old.")
        return False
    try:
        customer.accounts[account_type][selected].withdraw(amount)
    except KeyError:
        print("Cannont find that account.")


def account_deposit(customer, account_type):
    '''Takes the customer object from account management and the type of
    account to deposit money from that account.'''
    list_accounts(customer.accounts[account_type])
    selected, amount = get_amount()
    try:
        customer.accounts[account_type][selected].deposit(amount)
    except KeyError:
        print("Cannont find that account.")


def get_amount():
    '''Prompts the user to enter the account and the amount of money
    they'd like to change the account by.'''
    account_prompt = "Which account? "
    amount_prompt = "How much money? "
    selected_account = my_input(account_prompt)
    amount = my_input(amount_prompt)
    try:
        return int(selected_account), float(amount)
    except ValueError:
        return None, None


def list_accounts(customer_accounts):
    '''Simple function to list all accounts of a particular type
    specified by the customer_accounts paramenter'''
    for account in customer_accounts:
        print(customer_accounts[account])


def my_input(prompt):
    '''Takes a prompt and will use the builtin input() to ask the
    user for information requested in the prompt. Made this because
    it would reduce the amount of try and excepts I needed to type'''
    while True:
        try:
            attempt = input(prompt)
            return attempt
        except (KeyboardInterrupt, EOFError):
            print("\nRetry.")


class MyUnpickler(pickle.Unpickler):
    '''Unpickler subclass used to not allow os commands to be
    hidden in my pickled file'''

    def find_class(self, module, name):
        # Check if os objects had been pickled
        if module == "posix":
            raise pickle.UnpicklingError
        return getattr(bon, name)

if __name__ == "__main__":
    main()
