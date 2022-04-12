# Author - Oluwamayowa Adelaja (C20376476)
# Description - A program that models a banking system, allowing customers to open accounts and to perform transactions on these accounts

#imports
from datetime import date #https://www.programiz.com/python-programming/datetime/current-datetime

class Account(object):
    """ Class that represents a bank account """

    def __init__(self, customer: object, acc_number: int, balance: int = 0):
        """ Method to initialise new instances, takes 3 parameters: customer object, account number and balance """

        #all the attributes are private so the cannot be changed externally or accessed directly
        self.__acc_number = acc_number
        self.__balance = int(balance)
        self.__customer = customer
        self.__transactions = []

        #if user has transactions in the transaction file, append them to their list of transactions
        try:
            with open("accountsTransactions.txt", "r") as file:
                for line in file:
                    line_list = line.split("-")
                    line_str = " ".join(line_list)
                    line_list = line_str.split()
                    if int(line_list[0]) == int(self.get_acc_number()):
                        self.get_transactions().append((line_list[1], line_list[2], line_list[3], line_list[4], line_list[5], line_list[6]))
        except IOError:
            print("\nError loading transactions from file\n")

    def __str__(self):
        """ Method for when the user tries to print the object """

        #account number appended to the output string
        result = "Account number: " + str(self.get_acc_number()) + "\n"
        #balance appended to the output string
        result += "Balance: " + str(self.get_balance()) + "\n"
        #customer object that is associated with the account has it's details printed using the customer object's __str__ method
        result += "Customer: " + str(self.get_customer().__str__())

        counter = 0

        #transactions are appended to the string
        result += "\nTransactions: \n"
        for trans in self.get_transactions():
            counter += 1
            result += "#" + str(counter) + "TransationID: " + str(trans[5]) +" Type: " + trans[0] + " - Amount: " + str(trans[1]) + " - Date: " + "{}-{}-{}".format(trans[2], trans[3], trans[4]) + "\n"

        #finished string is returned
        return result

    def __add__(self, amount:int):
        """ operator overload used as a shortcut for deposit method """

        #deposit method is called and a success or error message is returned
        return self.deposit(amount)

    def __sub__(self, amount:int):
        """ operator overload used as a shortcut for the withdraw method """

        #withdraw method is called and a success or error message is returned
        return self.withdraw(amount)

    def get_acc_number(self):
        """ method used to retrieve the private acc_number attribute """

        return str(self.__acc_number)

    def get_balance(self):
        """ method used to retrieve the private balance attribute """

        return str(self.__balance)

    def set_balance(self, value: int):
        """ method used to set the private balance attribute """

        self.__balance = value

    def get_customer(self):
        """ method used to retrieve the private customer attribute """

        return self.__customer

    def get_transactions(self):
        """ method used to retrieve the private transactions attribute """

        return self.__transactions

    def show_transactions(self):
        """ method to display the transactions of the account """

        #if the length of the list is 0 there are no transactions present
        if len(self.get_transactions()) == 0:
            return "\nYou have no transactions on this acccount"

        #counter used to keep track of the transaction number
        counter = 0

        result = "\nTransactions: \n"

        #for loop to append all the transactions and their details to a string
        for trans in self.get_transactions():
            counter += 1
            result += "#" + str(counter) + "TransationID: " + str(trans[5]) + " Type: " + trans[0] + " - Amount: " + str(trans[1]) + " - Date: " + "{}-{}-{}".format(trans[2], trans[3], trans[4]) + "\n"

        #returning the resulting string
        return result

    def withdraw(self, amount: int):
        """ method for withdrawing money from the account """

        #if statement to make sure the amount entered is positive
        if int(amount) <= 0:
            print("You can only withdraw a positive value")
            return

        #getting today's date
        date_list = today_date()

        #counter used in making a unique transactionID
        counter = 0

        #counting the number of lines in the transaction file
        try:
            with open("accountsTransactions.txt", "r") as file:
                for line in file:
                    counter += 1

            #creating a tuple to hold the transaction details
            transaction = ("withdraw", amount, date_list[0], date_list[1], date_list[2], 100+counter)

            #reading the data in the transaction file
            with open("accountsTransactions.txt", "r") as file:
                data = file.read()

            #adding the transaction to the transaction file
            #if the file is empty append the string, if the file is not empty add a newline and then append the string
            with open("accountsTransactions.txt", "a") as file:
                if len(data) > 0:
                    file.write("\n")
                file.write("{} {} {} {}-{}-{} {}".format(self.get_acc_number(), transaction[0], transaction[1], date_list[0], date_list[1], date_list[2], transaction[5]))

            #appending the transaction to the transaction list of the user
            self.get_transactions().append(transaction)

            #setting the new balance of the user
            self.set_balance(int(self.get_balance()) - int(amount))

        except IOError:
            print("\nError reading/writing with file, transaction not completed\n")

    def deposit(self, amount: int):
        """ method to deposit money into the account """

        #making sure the amount is a positive value
        if int(amount) <= 0:
            print("You can only deposit a positive value")
            return

        #getting today's date
        date_list = today_date()

        #counter used in making a unique transactionID
        counter = 0

        #counting the number of lines in the transaction file
        try:
            with open("accountsTransactions.txt", "r") as file:
                for line in file:
                    counter += 1

            #creating a tuple to hold the transaction details
            transaction = ("deposit", amount, date_list[0], date_list[1], date_list[2], 100+counter)

            #reading the data in the transaction file
            with open("accountsTransactions.txt", "r") as file:
                data = file.read()

            #adding the transaction to the transaction file
            #if the file is empty append the string, if the file is not empty add a newline and then append the string
            with open("accountsTransactions.txt", "a") as file:
                if len(data) > 0:
                    file.write("\n")
                file.write("{} {} {} {}-{}-{} {}".format(self.get_acc_number(), transaction[0], transaction[1], date_list[0], date_list[1], date_list[2], transaction[5]))

            #appending the transaction to the transaction list of the user
            self.get_transactions().append(transaction)

            #setting the new balance of the account
            self.set_balance(int(self.get_balance()) + int(amount))

        except IOError:
            print("\nError reading/writing with file, transaction not completed\n")

    def transfer(self, receiver: object, amount: int):
        """ method for transferring to a new account """

        #checking that the amount is positive
        if int(amount) <= 0:
            print("You can only transfer a positive value")
            return

        #getting today's date
        date_list = today_date()

        #counter used in making a unique transactionID
        counter = 0

        #counting the number of lines in the transaction file
        try:
            with open("accountsTransactions.txt", "r") as file:
                for line in file:
                    counter += 1

            #creating a tuples to hold the details of both transactions, e.g. account sending and account receiving
            transaction = ("transferOut", amount, date_list[0], date_list[1], date_list[2], 100+counter)
            transaction2 = ("transferIn", amount, date_list[0], date_list[1], date_list[2], 100+counter)

            #reading the data in the transaction file
            with open("accountsTransactions.txt", "r") as file:
                data = file.read()

            #adding the transaction to the transaction file
            #if the file is empty append the string, if the file is not empty add a newline and then append the string
            with open("accountsTransactions.txt", "a") as file:
                if len(data) > 0:
                    file.write("\n")
                file.write("{} {} {} {}-{}-{} {}".format(self.get_acc_number(), transaction[0], transaction[1], date_list[0], date_list[1], date_list[2], transaction[5]))

            #reading the data in the transaction file
            with open("accountsTransactions.txt", "r") as file:
                data = file.read()

            #adding the transaction to the transaction file
            #if the file is empty append the string, if the file is not empty add a newline and then append the string
            with open("accountsTransactions.txt", "a") as file:
                if len(data) > 0:
                    file.write("\n")
                file.write("{} {} {} {}-{}-{} {}".format(receiver.get_acc_number(), transaction2[0], transaction2[1], date_list[0], date_list[1], date_list[2], transaction2[5]))

            #appending the transaction to the transaction list of both users
            self.get_transactions().append(transaction)
            receiver.get_transactions().append(transaction2)

            #setting the new balance of both users
            self.set_balance(int(self.get_balance()) - int(amount))
            receiver.set_balance(int(receiver.get_balance()) + int(amount))

        except IOError:
            print("\nError reading/writing with file, transaction not completed\n")

class SavingsAccount(Account):
    """ Class for Savings Accounts """

    def __init__(self, customer: object, acc_number: int, balance: int):
        """ Method to initialise new instances, takes 3 parameters: customer object, account number and balance """
        
        #using the Account Class' __init__ method and then adding another attribute particular to this Savings Account class
        Account.__init__(self, customer, acc_number, balance)
        self.__type = "Savings"

    def __str__(self):
        """ Method for when the user tries to print the object """

        #using inheritance and using the __str__ method of the parent class and also adding an extra bit particular to this class
        return Account.__str__(self) + "Account Type: {}\n".format(self.get_type())

    def get_type(self):
        """ method to get the private attribute 'type' """

        #return the attribute 'type'
        return self.__type

    def withdraw(self, amount:int):
        """ method for withdrawing money from the account """

        #if their are no transactions in the account make the transaction
        if len(self.get_transactions()) == 0:
            #calling the withdraw method of the parent class
            Account.withdraw(self, amount)
            #function to update the external file
            update_accounts_file()
            #return success message
            return "\nTransaction Successful\n"

        #get today's date
        today_list = today_date()

        #if today's month matches the montg=h of the latest transaction of the account do not allow the transaction
        if str(today_list[1]) == str(self.get_transactions()[len(self.get_transactions())-1][3]):
            #returning error message
            return "Can only make one transfer/withdrawal per month with a savings account"

        #calling the withdraw method of the parent class
        Account.withdraw(self, amount)
        #function to update the external file
        update_accounts_file()
        #return success message
        return "\nTransaction Successful\n"

    def deposit(self, amount:int):
        """ method to deposit into the account """
        
        #calling the deposit method of the parent account
        Account.deposit(self, amount)
        #update external file
        update_accounts_file()
        #return success message
        return "\nTransaction Successful\n"

    def transfer(self, receiver: object, amount: int):
        """ method to transfer money to another account """

        #if their are no transactions in the account make the transaction
        if len(self.get_transactions()) == 0:
            #calling transfer method of parent class
            Account.transfer(self, receiver, amount)
            #updating the external file
            update_accounts_file()
            #returning success message
            return "\nTransaction Successful\n"

        #getting today's date
        today_list = today_date()

        #if today's month matches the montg=h of the latest transaction of the account do not allow the transaction
        if str(today_list[1]) == str(self.get_transactions()[len(self.get_transactions())-1][3]):
            #return error message
            return "Can only make one transfer/withdrawal per month with a savings account"

        #calling the transfer method of the parent class
        Account.transfer(self, receiver, amount)
        #updating external file
        update_accounts_file()
        #return success message
        return "\nTransaction Successful\n"

class CheckingAccount(Account):
    """ class representing a Checking Account """

    def __init__(self, customer: object, acc_number: int, balance: int):
        """ Method to initialise new instances, takes 3 parameters: customer object, account number and balance """
        Account.__init__(self, customer, acc_number, balance)
        self.__type = "Checking"

    def __str__(self):
        """ Method for when the user tries to print the object """

        #using inheritance and using the __str__ method of the parent class and also adding an extra bit particular to this class
        return Account.__str__(self) + "Account Type: {}\n".format(self.get_type())

    def get_type(self):
        """ method to get the private attribute 'type' """

        #return the attribute 'type'
        return self.__type

    def withdraw(self, amount:int):
        """ method to withdraw money from the account """

        #if the transaction would cause the balance to go below the credit limit do not allow it
        if int(self.get_balance()) - int(amount) < credit_limit:
            #return error message
            return "\nTransaction prohibited as it would lead to a balance below the credit limit\n"

        #calling the withdraw method of the parent class
        Account.withdraw(self, amount)
        #updating external accounts
        update_accounts_file()
        #return success message
        return "\nTransaction Successful\n"

    def deposit(self, amount:int):
        """ method to deposit money into the account """

        #calling the deposit method of the parent class
        Account.deposit(self, amount)
        #update external file
        update_accounts_file()
        #return success message
        return "\nTransaction Successful\n"

    def transfer(self, receiver: object, amount: int):
        """ method to transfer money to another account """

        #if the transaction would cause the balance to go below the credit limit do not allow it
        if int(self.get_balance()) - int(amount) < credit_limit:
            #return error message
            return "\nTransaction prohibited as it would lead to a balance below the credit limit\n"

        #calling the transfer method of the parent class
        Account.transfer(self, receiver, amount)
        #update external file
        update_accounts_file()
        #retunr success message
        return "\nTransaction Successful\n"

class Customer(object):
    """ class to represent a customer """

    def __init__(self, customer_id: int, firstname: str = "", surname: str = "", age: int = 0):
        """ Method to initialise new instances, takes 4 parameters: customerID, firstname, surname and age """
        self.__customer_id = customer_id
        self.__firstname = firstname
        self.__surname = surname
        self.__age = age

    def __str__(self):
        """ Method for when the user tries to print the object """

        #returning a string with all the info of the customer
        return "Your customer ID is {}\nYour name is {} {}\nYour age is {}\n".format(str(self.get_id()), str(self.get_firstname()), str(self.get_surname()), str(self.get_age()))

    def get_firstname(self):
        """ method to get the private firstname attribute """

        #return the firstname
        return self.__firstname

    def get_surname(self):
        """ method to get the private surname attribute """

        #return the surnmae
        return self.__surname

    def get_age(self):
        """ method to get the private age attribute """

        #return the age
        return self.__age

    def get_id(self):
        """ method to get the private ID attribute """

        #return the customerID
        return self.__customer_id


def create_customers() -> list:
    """ function to create the customers using the external file """

    #initialising a dictionary and list that will be used
    customers_dict = {}
    customer_list = []

    try:
        #read from the file and assign the values into a dictionary
        with open("customers.txt", "r") as file:
            for line in file:
                line_list = line.split()
                customers_dict[line_list[0]] = (line_list[1], line_list[2], line_list[3])

        #append the Customer instances to a list that can be used later
        for key in customers_dict.keys():
            customer_list.append(Customer(int(key), customers_dict[key][0], customers_dict[key][1], int(customers_dict[key][2])))

        #return the list of customer instances
        return customer_list

    except IOError:
            print("\nError reading from the file, transaction not completed\n")
            return


def create_accounts(customers: list) -> list:
    """ method to create the accounts using a file """

    #initialising a dictionary and list that will be used
    accounts_dict = {}
    account_list = []

    try:
        #read from the file and assign the values into a dictionary
        with open("accounts.txt", "r") as file:
            for line in file:
                line_list = line.split()
                accounts_dict[line_list[0]] = (line_list[1], line_list[2], line_list[3])

        for key in accounts_dict.keys():
            for cust in customers:
                #if the customer ID associated with the account matches a customerID in the list of customers continue
                if str(accounts_dict[key][0]) == str(cust.get_id()):
                    #if the type of account listed in the file is 'Savings' create a savings account
                    if accounts_dict[key][1] == "Savings":
                        account_list.append(SavingsAccount(cust, int(key), accounts_dict[key][2]))
                    #if the type of account listed in the file is 'Checking' create a checking account
                    elif accounts_dict[key][1] == "Checking":
                        account_list.append(CheckingAccount(cust, int(key), accounts_dict[key][2]))

        #return the list of accounts
        return account_list

    except IOError:
            print("\nError reading from the file, transaction not completed\n")
            return


def create_account(user: object):
    """ function for a customer to create an account """

    #variables to keep track of if the user has a saving and/or checking account
    checking_count = 0
    savings_count = 0

    #for loop to note if the user has a checking and/or saving account
    for x in accounts:
        if user == x.get_customer() and x.get_type() == "Savings":
            savings_count += 1
        if user == x.get_customer() and x.get_type() == "Checking":
            checking_count += 1

    #if user has a checking account offer them to create a savings account
    if checking_count == 1 and savings_count == 0:
        user_input = input("You can create a savings account, enter 'Y' to do so: ")
        if user_input == 'Y':
            create_savings(user)

    #if user has a checking account offer them to create a checking account
    elif checking_count == 0 and savings_count == 1:
        user_input = input("You can create a checking account, enter 'Y' to do so: ")
        if user_input == 'Y':
            create_checking(user)

    #if user already has both accounts
    elif checking_count == 1 and savings_count == 1:
        print("You already have a checking and a savings account")

    #if user has neither offer them the option to create a checking or savings account
    elif checking_count == 0 and savings_count == 0:
        user_input = input("You have no account, enter '1' to create a savings account and '2' to create a checking account: ")

        #if user inputs 1 create a savings account
        if user_input == '1':
            create_savings(user)

        #if user inputs 2 create a checking account
        elif user_input == '2':
            create_checking(user)

    else:
        return

def create_checking(user: object):
    """ function to create a checking account """

    #if the user is under 18 they cannot make the account
    if int(user.get_age()) < 18:
        print("\nToo young to open a checking account\n")
        return

    try:
        #read the accounts file
        with open("accounts.txt", "r") as file:
            data = file.read()

        #add the new account to the account file
        #if the file is empty append the string, if the file is not empty add a newline and then append the string
        with open("accounts.txt", "a") as file:
            if len(data) > 0:
                file.write("\n")
            file.write("{} {} {} {}".format(int(accounts[len(accounts) - 1].get_acc_number()) + 1, user.get_id(), "Checking", 0))

        #append the new account to the accounts list
        accounts.append(CheckingAccount(user, int(accounts[len(accounts) - 1].get_acc_number()) + 1, 0))

    except IOError:
            print("\nError reading/writing with the file, account not created\n")
            return

def create_savings(user: object):
    """ function to create a savings account """

    #if the user is under 14 they cannot make the account
    if int(user.get_age()) < 14:
        print("\nToo young to open a savings account\n")
        return

    try:
        #read the accounts file
        with open("accounts.txt", "r") as file:
            data = file.read()

        #add the new account to the account file
        #if the file is empty append the string, if the file is not empty add a newline and then append the string
        with open("accounts.txt", "a") as file:
            if len(data) > 0:
                file.write("\n")
            file.write("{} {} {} {}".format(int(accounts[len(accounts) - 1].get_acc_number()) + 1, user.get_id(), "Savings", 0))

        #append the new account to the accounts list
        accounts.append(SavingsAccount(user, int(accounts[len(accounts) - 1].get_acc_number()) + 1, 0))

    except IOError:
            print("\nError reading/writing with the file, account not created\n")
            return

def update_accounts_file():
    """ function to update the file holding the accounts """

    try:
        #overwrite everything in the file with the updated information of the accounts
        with open("accounts.txt", "w") as file:
            #getting the length of the accounts
            length = len(accounts)
            #counter used to know when to stop adding newlines
            counter = 0
            #for loop to write the information into the file
            for x in accounts:
                counter += 1
                if counter != length:
                    file.write("{} {} {} {}\n".format(x.get_acc_number(), x.get_customer().get_id(), x.get_type(), x.get_balance()))
                else:
                    file.write("{} {} {} {}".format(x.get_acc_number(), x.get_customer().get_id(), x.get_type(), x.get_balance()))

    except IOError:
            print("\nError writing to the file, accounts.txt not updated\n")
            return

def login() -> object:
    """ function for the user to login if they are a customer """

    #user enters their customerID
    input_id = input("\nEnter your Customer ID: ")

    try:
        #check if the input was a number
        input_id = int(input_id)

    except ValueError:
        #error message
        print("\nYou did not enter a number")
        #error code that is used later
        return 1
    
    #if a success, get the customer object associated with that customerID and return the object so that it can be used elsewhere
    for x in customers:
        #cycle through the customers looking for a match
        if int(x.get_id()) == int(input_id):
            #success message
            print("Login Successful")
            #return the customer object
            return x

    #return error code if no match is found
    return 1

#https://www.programiz.com/python-programming/datetime/current-datetime
def today_date() -> list:
    """ function to get the date and return it as a list """

    #using tthe date function that was imported
    today = str(date.today())
    #split the values
    date_list = today.split("-")
    #return the values in a list
    return date_list

def select_account(user: object) -> object:
    """ function to select an existing account """

    #variables to keep track of if the user has a saving and/or checking account
    savings_count = 0
    checking_count = 0

    #for loop to note if the user has a checking and/or saving account
    for x in accounts:
        if user == x.get_customer() and x.get_type() == "Savings":
            savings_count += 1
        if user == x.get_customer() and x.get_type() == "Checking":
            checking_count += 1

    #if user has a checking account let them choose this account
    if checking_count == 1 and savings_count == 0:
        user_input = input("You can choose your checking account as it is the only account you have, enter 'Y' to do so: ")
        if user_input == 'Y':
            for x in accounts:
                #returning the checking account
                if user == x.get_customer() and x.get_type() == "Checking":
                    return x

    #if user has a savings account let them choose this account
    elif checking_count == 0 and savings_count == 1:
        user_input = input("You can choose your savings account as it is the only account you have, enter 'Y' to do so: ")
        if user_input == 'Y':
            for x in accounts:
                #returning the savings account
                if user == x.get_customer() and x.get_type() == "Savings":
                    return x

    #if the user has both accounts allow them to choose either
    elif checking_count == 1 and savings_count == 1:
        user_input = input("Enter '1' to choose your savings account and '2' for your checking account: ")
        if user_input == '1':
            for x in accounts:
                #returning the savings account
                if user == x.get_customer() and x.get_type() == "Savings":
                    return x
        elif user_input == '2':
            for x in accounts:
                #returning the checking account
                if user == x.get_customer() and x.get_type() == "Checking":
                    return x
        else:
            print("Input error")
            return 

    #if user has no account
    elif checking_count == 0 and savings_count == 0:
        #print error message
        print("\nYou have no account")
        return 

    else:
        return 

def account_exists(user: object, account_id: int) -> object:
    """ function to check if account exists """


    for x in accounts:
        #checking if the accountID inputted by the user matches an accountID that exists
        if int(account_id) == int(x.get_acc_number()):
            if x.get_customer() == user:
                #if the accountID is associated with the customer don't allow the transfer and print error message
                print("\nCannot transfer to yourself\n")
                return
            #if check is successful return that account object
            return x
    return

def create_customer():
    """ function to create a customer """

    #getting the firstname and surname
    firstname = input("Enter your firstname: ")
    surname = input("Enter your surname: ")

    #error checking for the age inputted
    while True:
        try:
            #user inputs age
            age = int(input("Enter an age: "))

        #if the age inputted was not a number
        except ValueError:
            print("\nYou did not enter a number\n")
        else:
            break

    try:
        #read data from the file
        with open("customers.txt", "r") as file:
            data = file.read()

        #adding the customer to the customer file
        #if the file is empty append the string, if the file is not empty add a newline and then append the string
        with open("customers.txt", "a") as file:
            if len(data) > 0:
                file.write("\n")
            file.write("{} {} {} {}".format(int(customers[len(customers) - 1].get_id()) + 1, firstname, surname, age))

        #print success message and tell the user their customerID
        print("\nAccount Created, your customerID is {}\n".format(int(customers[len(customers) - 1].get_id()) + 1))
        #append new Customer instance to the customers list
        customers.append(Customer(int(customers[len(customers) - 1].get_id()) + 1, firstname, surname, age))

    except IOError:
            print("\nError reading/writing with the file, account not created\n")
            return
    


def menu():
    """ function to run the menu """

    #while loop to keep the program running until the user decides to end it
    while True:
        #print options
        print("\n1. Log In\n2. New Customer? Sign Up!\n3. End Program")
        #user enters their choice
        menu_input = input("Choose 1, 2 or 3: ")
        #if user chooses '1'
        if menu_input == '1':
            #run the login function
            user = login()
            #if there is no error code returned
            if user != 1:
                #initialise the 2nd menu variable as 0
                menu_input2 = 0
                #while the input variable is not equal to the 7th option (Logout)
                while menu_input != '7':
                    #display menu and ask for user input
                    menu_input2 = input("\n1. Create a new account\n2. View transactions performed in one of your accounts and view the balance\n3. Deposit Money\n4. Transfer Money to a different account\n5. Withdraw Money from an account\n6. Delete an account\n7. Logout\n: ")
                    #if input is '1'
                    if menu_input2 == '1':
                        #call function to create account and pass the customer instance of the user as the paramter
                        create_account(user)
                    
                    #if menu input is '2'
                    if menu_input2 == '2':
                        #call function to select an account and pass the customer instance of the user as the paramter, result is assigned to a variable
                        user_account = select_account(user)
                        #if the variable contains something
                        if user_account != None:
                            #call the show transactions method of the account that was returned
                            print(user_account.show_transactions())
                            #show the balance of the account that was returned
                            print("Balance: {}".format(str(user_account.get_balance())))
                    
                    #if menu input is '3'
                    if menu_input2 == '3':
                        #call function to select an account and pass the customer instance of the user as the paramter, result is assigned to a variable
                        user_account = select_account(user)
                        #if the variable contains something
                        if user_account != None:
                            #error checking for the amount inputted
                            while True:
                                try:
                                    #user inputs amount
                                    amount = input("enter the amount you want to deposit: ")

                                #if the amount inputted was not a number
                                except ValueError:
                                    print("\nYou did not enter a number\n")
                                else:
                                    break
                            #use operator overload to perform the deposit method
                            print(user_account + amount)

                    #if menu input is '4'
                    if menu_input2 == '4':
                        #call function to select an account and pass the customer instance of the user as the paramter, result is assigned to a variable
                        user_account = select_account(user)
                        #if the variable contains something
                        if user_account != None:
                            #error checking for the amount inputted
                            while True:
                                try:
                                    #user inputs amount
                                    amount = input("enter the amount you want to transfer: ")

                                #if the amount inputted was not a number
                                except ValueError:
                                    print("\nYou did not enter a number\n")
                                else:
                                    break
                            #enter the accountID of the account you want to transfer to
                            account_id = input("Enter the ID of the account you want to tranfer to: ")
                            #check if the accountID exists
                            receiver = account_exists(user, account_id)
                            #if the variable is not empty
                            if receiver != None:
                                #call the transfer method
                                print(user_account.transfer(receiver, amount))
                    
                    #if menu input is '5'
                    if menu_input2 == '5':
                        #call function to select an account and pass the customer instance of the user as the paramter, result is assigned to a variable
                        user_account = select_account(user)
                        #if the variable contains something
                        if user_account != None:
                            #error checking for the amount inputted
                            while True:
                                try:
                                    #user inputs amount
                                    amount = input("enter the amount you want to withdraw: ")

                                #if the amount inputted was not a number
                                except ValueError:
                                    print("\nYou did not enter a number\n")
                                else:
                                    break
                            #use operator overload to perform the withdraw method
                            print(user_account - amount)
                    
                    #if menu input is '6'
                    elif menu_input2 == '6':
                        #call function to select an account and pass the customer instance of the user as the paramter, result is assigned to a variable
                        user_account = select_account(user)
                        #if variable contains something
                        if user_account != None:
                            #remove the account from the list of accounts
                            accounts.remove(user_account)
                            #print message
                            print("\nAccount Deleted\n")
                            #update the file of accounts
                            update_accounts_file()

                    #if menu input is '7'
                    elif menu_input2 == '7':
                        #break from the loop that keeps the menu going
                        break

                    #input validation
                    elif menu_input2 not in ['1', '2', '3', '4', '5', '6', '7']:
                        print("\nInvalid input")

            #print message if login was unsuccessful
            else:
                print("Login Unsuccessful")

        #if menu input is '2'
        elif menu_input == '2':
            #call function to create customer
            create_customer()

        #if menu input is '3'
        elif menu_input == '3':
            #break from loop
            break

        #input validation
        elif menu_input not in ['1', '2', '3']:
            print("\nInvalid Input")

#main
#initialising the credit limit
credit_limit = -100
#calling the functions to create the customers and accounts list and assign the return values (lists) to variables
customers = create_customers()
#customers list passed as a paramter to be used in creating accounts
accounts = create_accounts(customers)
#call the menu function
menu()
