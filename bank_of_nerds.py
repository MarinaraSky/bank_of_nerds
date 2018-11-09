#! /usr/bin/env python3
from bon_Classes import Checking, Savings, Customer, FourOhOneK
from getpass import getpass
import hashlib
import pickle


clear_screen = "\033c"

def main():
    startup()
    print(clear_screen)
    main_loop = True
    while main_loop:
        main_loop = menu_loop()
    shutdown()


def menu_loop():
    loop = True
    while loop:
        login_options = {'1': user_login, '2': new_customer,
                         '3': list_users, '9': None}
        login_menu = "1) Existing Customer.\n2) New User.\n" \
                     "3) List Users\n9) Quit.\n>"
        try:
            selection = login_options[my_input(login_menu)]
            if selection is None:
                shutdown()
                return
            loop = selection()
            # Used to end loop if customer is found
            if isinstance(loop, Customer):
                break
        except KeyError:
            print("Not a Valid option.")
    customer = loop
    loop = True
    while loop:
        loop = account_management(customer)
        my_input("Enter to Continue.")
        print(clear_screen)
    another = "Would you like to return to the main menu(Y/N)?\n>"
    selection = my_input(another)
    if selection.upper() == "Y":
        return True
    else:
        return False


def startup():
    loaded = [0, 0, 0, 0, None]
    try:
        file = open(".bon_database.jack", "rb")
        loaded = pickle.load(file)
        file.close()
        Checking.checking_id = loaded[0]
        Savings.savings_id = loaded[1]
        Customer.customer_id = loaded[2]
        FourOhOneK.four_oh_one_k_id = loaded[3]
        Customer.customers = loaded[4]
    except FileNotFoundError:  # Silently continue with default numbers
        pass


def shutdown():
    saving = [Checking.checking_id, Savings.savings_id, Customer.customer_id,
              FourOhOneK.four_oh_one_k_id, Customer.customers]
    with open(".bon_database.jack", "w+b") as file:
        pickle.dump(saving, file)


def list_users():
    for customer in Customer.customers:
        print("Customer", Customer.customers[customer])
        list_accounts(Customer.customers[customer].accounts['Checking'])
        list_accounts(Customer.customers[customer].accounts['Savings'])
        list_accounts(Customer.customers[customer].accounts['401k'])

    my_input("Enter to Continue.")
    print(clear_screen)
    return True


def new_customer():
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

    new = Customer(first_name, last_name, username, age)
    if new:
        # Loop Variable
        return True
    else:
        return False


def user_login():
    login_prompt = "Please enter your user ID.\n>"
    password_prompt = "Please enter your password.\n>"
    error_prompt = "Cannot log in.\n"
    login_attempt = my_input(login_prompt)
    try:
        if Customer.customers[login_attempt].password == hashlib.md5(
                getpass(password_prompt).encode("utf-8")).hexdigest():
            print("Success")
            return Customer.customers[login_attempt]
        else:
            print("Fail")
            return True
    except KeyError:
        print(error_prompt)
        return True


def account_management(selected_customer):
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
                {Checking.checking_id: Checking()})
    elif account_input == "2":
        selected_customer.accounts['Savings'].update(
                {Savings.savings_id: Savings()})
    elif account_input == "3":
        selected_customer.accounts['401k'].update(
                {FourOhOneK.four_oh_one_k_id: FourOhOneK()})
    elif account_input == "4":
        checking_deposit(selected_customer)
    elif account_input == "5":
        savings_deposit(selected_customer)
    elif account_input == "6":
        four_oh_one_k_deposit(selected_customer)
    elif account_input == "7":
        checking_withdraw(selected_customer)
    elif account_input == "8":
        savings_withdraw(selected_customer)
    elif account_input == "9":
        four_oh_one_k_withdraw(selected_customer)
    elif account_input == "10":
        list_accounts(selected_customer.accounts['Checking'])
        list_accounts(selected_customer.accounts['Savings'])
        list_accounts(selected_customer.accounts['401k'])
    return True


def checking_withdraw(customer):
    list_accounts(customer.accounts['Checking'])
    selected, amount = get_amount()
    try:
        customer.accounts['Checking'][selected].withdraw(amount)
    except KeyError:
        print("Cannont find that account.")


def savings_withdraw(customer):
    list_accounts(customer.accounts['Savings'])
    selected, amount = get_amount()
    try:
        customer.accounts['Savings'][selected].withdraw(amount)
    except KeyError:
        print("Cannont find that account.")


def four_oh_one_k_withdraw(customer):
    list_accounts(customer.accounts['401k'])
    if customer.age < 67:
        print("Too young to withdraw from 401k.")
        return
    selected, amount = get_amount()
    try:
        customer.accounts['401k'][selected].withdraw(amount)
    except KeyError:
        print("Cannont find that account.")


def four_oh_one_k_deposit(customer):
    list_accounts(customer.accounts['401k'])
    selected, amount = get_amount()
    try:
        customer.accounts['401k'][selected].deposit(amount)
    except KeyError:
        print("Cannont find that account.")


def checking_deposit(customer):
    list_accounts(customer.accounts['Checking'])
    selected, amount = get_amount()
    try:
        customer.accounts['Checking'][selected].deposit(amount)
    except KeyError:
        print("Cannont find that account.")


def savings_deposit(customer):
    list_accounts(customer.accounts['Savings'])
    selected, amount = get_amount()
    try:
        customer.accounts['Savings'][selected].deposit(amount)
    except KeyError:
        print("Cannont find that account.")


def get_amount():
    account_prompt = "Which account? "
    amount_prompt = "How much money? "
    selected_account = my_input(account_prompt)
    amount = my_input(amount_prompt)
    try:
        return int(selected_account), float(amount)
    except ValueError:
        return None, None


def list_accounts(customer_accounts):
    for account in customer_accounts:
        print(customer_accounts[account])


def my_input(prompt):
    while True:
        try:
            attempt = input(prompt)
            return attempt
        except (KeyboardInterrupt, EOFError):
            print("\nRetry.")


if __name__ == "__main__":
    main()
