#Bank of nerds MAIN
# Change * h
from bon_Classes import Checking, Savings, Customer
from getpass import getpass

def main():

    loop = True
    while loop:
        login_options = {'1': user_login, '2': new_customer, '9': exit}
        login_menu = "1) Existing Customer.\n2) New User.\n9) Quit.\n>"
        try:
            selection = login_options[my_input(login_menu)]
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


def new_customer():
    first_name_prompt = "Please enter your first name.\n>"
    last_name_prompt = "Please enter your last name.\n>"
    username_prompt = "Please enter your desired username.\n>"
    age_prompt = "Please enter your age.\n>"

    first_name = my_input(first_name_prompt)
    last_name = my_input(last_name_prompt)
    username = my_input(username_prompt)
    age = my_input(age_prompt)

    new = Customer(first_name, last_name, username, age)
    if new:
        #Loop Variable
        return True
    else:
        return False

def user_login():
    login_prompt = "Please enter your user ID.\n>"
    password_prompt = "Please enter your password.\n>"
    error_prompt = "Cannot log in.\n"
    login_attempt = my_input(login_prompt)
    try:
        if Customer.customers[login_attempt].password == hash(getpass(password_prompt)):
            print("Success")
            return Customer.customers[login_attempt]
        else:
            print("Fail")
            return True
    except KeyError:
        print(error_prompt)
        return True

def account_management(selected_customer):
    account_prompt = "1) New Checking\n2) New Savings\n3) Deposit Checking\n" \
            "4) Savings Deposit\n5) Checking Withdraw\n6) Savings Withdraw\n" \
            "7) List Balances\n9) Exit\n>"
    account_input = my_input(account_prompt)
    if account_input == "9":
        return False
    elif account_input == "1":
        selected_customer.accounts['Checking'].update({Checking.checking_id: Checking()})
    elif account_input == "2":
        selected_customer.accounts['Savings'].update({Savings.savings_id: Savings()})
    elif account_input == "3":
        checking_deposit(selected_customer)
    elif account_input == "4":
        savings_deposit(selected_customer)
    elif account_input == "5":
        checking_withdraw(selected_customer)
    elif account_input == "6":
        savings_withdraw(selected_customer)
    elif account_input == "7":
        list_accounts(selected_customer.accounts['Checking'])
        list_accounts(selected_customer.accounts['Savings'])

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
            print("Retry.")



if __name__ == "__main__":
    main()
