#Bank of nerds MAIN
# Change * h
from bon_Classes import Account, Customer
from getpass import getpass

def main():

    loop = True
    while loop == True:
        login_options = {'1': user_login, '2': new_customer, '9': exit}
        login_menu = "1) Existing Customer.\n2) New User.\n9) Quit.\n>"
        try:
            selection = login_options[my_input(login_menu)]
            loop = selection()
        except KeyError:
            print("Not a Valid option.")


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
            account_management(Customer.customers[login_attempt])
        else:
            print("Fail")
    except KeyError:
        print(error_prompt)
        return False



def my_input(prompt):
    while True:
        try:
            attempt = input(prompt)
            return attempt
        except (KeyboardInterrupt, EOFError):
            print("Retry.")



if __name__ == "__main__":
    main()
