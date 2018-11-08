#Bank of nerds MAIN
# Change * h
from bon_Classes import Account, Customer

def main():
    login_options = {'1': None, '2': new_customer}
    login_menu = "1) Existing Customer.\n2) New User.\n>"
    selection = login_options[my_input(login_menu)]
    selection()


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

def my_input(prompt):
    while True:
        try:
            attempt = input(prompt)
            return attempt
        except (KeyboardInterrupt, EOFError):
            print("Retry.")



if __name__ == "__main__":
    main()
