#!/bin/usr/env python3
import os
import time
import sys


class Account:
    """ The account class contains the methods of depositing or """
    """ withdrawing.  It stores a float and a product label """

    def __init__(self, product):
        self.balance = 0.00
        self.product = product
    # withdraw and deposit are stored with the account because the accoount
    # possess the items being deposited and withdrawn

    def withdraw(self, withdraw):
        self.balance = self.balance-withdraw

    def deposit(self, deposit):
        self.balance = self.balance+deposit


class MoneyMarket(Account):

    """ Money Market Accounts has a withdrawLimit, and a unique withdraw """
    """ method """

    def __init__(self, product):
        super().__init__(product)
        self.withdrawLimit = 2

    def withdraw(self, withdraw):
        if self.withdrawLimit == 0:
            print("\tYou must wait until next month to withdraw from"
                  "\tyour money market account")
        else:
            self.balance = self.balance-withdraw
            self.withdrawLimit -= 1


class Customer:

    """ the customer class contains all of the pertinent information for """
    """ customers accounts, name, age, idnum, numAccounts, currAccount """
    """ and accounts """

    def __init__(self, name, age, idnum):
        self.name = name
        self.age = age
        self.id = idnum
        # used to keep track of the customers number of accounnts, and to
        # assign each account a unique id
        self.numAccounts = 0
        self.accounts = {}
        # currAccount stores the account the user has selected from which to
        # deposit or withdraw
        self.currAccount = Account("Savings")

    def listAccounts(self):
        """ The customers dictionary key, and account information is """
        """ formated, appended to a list, and the list is then returned """
        """ to the teller """
        accountList = []
        accountView = "{0} : {1} ${2:.2f}"
        for product, accounts in self.accounts.items():
            accountList.append(accountView.format(product, accounts.product,
                                                  accounts.balance))
        return accountList

    def __str__(self):
        """ The foramt strings prints all of the custoers relevant """
        """ bank information """
        userView = "Customer#{0}  Name: {1} Age: {2}  Accounts: {3}"
        return userView.format(self.id, self.name, self.age, self.numAccounts)


class Bank:
    # Used to assign each customer a unique id
    clientId = 0
    """ the Bank has the ability to create accounts, create new clients """
    """ and list clients """

    def __init__(self):
        self.clients = {}
        # The bank has a teller, and the teller has a bank. While this may
        # seem cyclical, it is necessary for the architecture of the program
        # as well as a bank. The teller acts as the interface to the bank
        # for the customer, and the teller acts as an interface to the customer
        # for the bank
        self.teller = Teller(self)

    def newClient(self, name, age):
        """ This method recieves the age and name of the customer from the """
        """ teller and then uses that information plus the unique id to """
        """ create a client, it then sets the newClient as the tellers """
        """ currCustomer """
        newClient = Customer(name, age, self.clientId)
        self.clients.update({self.clientId: newClient})
        self.clientId += 1
        # sets the client just created as the tellers current customer
        self.teller.currCustomer = newClient
        # calls the tellers select product method
        self.teller.selectProduct()

    def createAccount(self, product):
        """ The bank receves the product the customer wants to create from """
        """ the teller, then uses that information to create an account """
        """ for the customer """
        if product == "Money Market":
            newAccount = MoneyMarket(product)
        else:
            newAccount = Account(product)
        self.teller.currCustomer.currAccount = newAccount
        self.teller.currCustomer.numAccounts += 1
        # setting the unique id of the account just created
        accountId = self.teller.currCustomer.numAccounts
        self.teller.currCustomer.accounts.update({accountId: newAccount})
        self.teller.accountActions()

    def listClients(self):
        """ listClients appends each customers str method to a list which """
        """ is then returned to the teller """
        customerList = []
        for idNums, customer in self.clients.items():
            customerList.append(customer.__str__())
        return customerList


class Teller:
    # used to print menu and product options
    productDict = {1: "Savings", 2: "Checkings", 3: "Retirement",
                   4: "Money Market"}
    actionList = ["A: Deposit", "B: Withdraw", "C: Create Account",
                  "D: List Accounts", "E: Main Menu"]

    def __init__(self, bank):
        # again, the teller needs access to the banks methods in order to
        # properly do their job
        self.bank = bank
        # a skeleton customer is initially set to the tellers currCustomer
        self.currCustomer = Customer(0, 0, 0)
        # options is a dictionary where the value are methods within the teller
        self.options = {}
        self.options['a'] = self.newCustomer
        self.options['b'] = self.selectCustomer
        self.options['c'] = self.goodBye
        # actions is a diictionary where the values are methods within the
        # teller
        self.actions = {}
        self.actions['a'] = self.deposit
        self.actions['b'] = self.withdraw
        self.actions['c'] = self.selectProduct
        self.actions['d'] = self.listAccounts
        self.actions['e'] = self.welcome

    def welcome(self):
        """ welcome "welcomes" the customer to the bank by printing the """
        """ tellers str, and presenting them with menu options """
        print("\tWelcome to the bank_of_nerds")
        userInput = self.valueValidation(self.__str__(), str)
        # The teller tries to perform the users request by getting the value
        # of the key selected, if the value is not present, the teller
        # will explain to them it is not available
        self.options.get(userInput.lower(), self.welcErr)()

    def newCustomer(self):
        """ new Customer wraps the banks new Client method, the teller """
        """ collects the customers relevant information and then passes """
        """ the information to the bank """
        name = self.valueValidation("What is your name? ", str)
        age = self.valueValidation("What is your age? ", int)
        self.bank.newClient(name, age)

    def selectProduct(self):
        """ select product lists the available products the bank has to """
        """ offer, and allows the user to select what they would like to """
        """ create, the product selection is then passed on to the bank"""
        os.system("clear")
        print(self.currCustomer.__str__())
        for key, value in Teller.productDict.items():
            print(key, ":", value)
        productKey = self.valueValidation("What kind of account "
                                          "would you like to open? ", int)
        # if the customer does not select an appropriate product they sent
        # back to the product listing and asked to choose again
        product = Teller.productDict.get(productKey, None)
        if product is None:
            self.selectProduct()
        self.bank.createAccount(product)

    def accountActions(self):
        """ accountActions offers the customer will all of the possible """
        """ Actions they can perform on the account. Once they have chose """
        """ the teller will refer to their own method of servicing their """
        """ needs """
        print(self.currCustomer.__str__())
        for items in Teller.actionList:
            print(items)
        action = self.valueValidation("What would you like to do? ", str)
        os.system("clear")
        # if the users selectio is not present, the teller explains to them
        # the action is not available and brings them back to available
        # actions
        self.actions.get(action.lower(), self.actErr)()

    def selectCustomer(self):
        """ selectCustomer wraps the banks list clients method. The """
        """ teller will check and make sure that the bank has clients """
        """ if so, it will allow the customer to select from that list """
        if len(self.bank.clients) == 0:
            os.system("clear")
            print("\tWe don't have any customers yet")
            self.welcome()
        else:
            customerList = self.bank.listClients()
            for customer in customerList:
                print(customer)
            customerId = self.valueValidation("Which customer would you "
                                              "like to access? ", int)
        self.currCustomer = self.bank.clients.get(customerId, None)
        if self.currCustomer is None:
            self.selectCustomer()
        os.system("clear")
        self.accountActions()

    def deposit(self):
        """ This method wraps the accounts deposit method """
        self.accountSelection()
        deposit = self.valueValidation("How much would you"
                                       " like to deposit? ", float)
        if deposit < 0:
            print("\tyou can not deposit negative amounts")
            self.accountActions()
        self.currCustomer.currAccount.deposit(deposit)
        os.system("clear")
        self.accountActions()

    def withdraw(self):
        """ This method wraps the accounts withdraw method """
        self.accountSelection()
        # error handling for retirement funds
        if self.currCustomer.currAccount.product == "Retirement" and\
                                                    self.currCustomer.age < 67:
            os.system("clear")
            print("You are not old enough to pull from your retirement")
            self.accountActions()
        withdraw = self.valueValidation("How much would"
                                        " you like to withdraw? ", float)
        if withdraw < 0:
            print("\tYou can not withdraw negative amounts")
            self.accountActions()
        # error handling for overdraft
        if (self.currCustomer.currAccount.balance - withdraw) < 0:
            os.system("clear")
            print("You do not have enough money to withdraw that amount")
            self.accountActions()
        self.currCustomer.currAccount.withdraw(withdraw)
        self.accountActions()

    def listAccounts(self):
        """ listAccounts wraps the customers listAccounts method """
        accountList = self.currCustomer.listAccounts()
        for account in accountList:
            print(account)
        self.accountActions()

    def accountSelection(self):
        """ account Selection wraps the tellers listAccounts method """
        """ this method is used for the customer to select which account """
        """ they wish to open """
        accountList = self.currCustomer.listAccounts()
        for item in accountList:
            print(item)
        account = self.valueValidation("Which account would"
                                       " you like to choose? ", int)
        currAccount = self.currCustomer.accounts.get(account, None)
        self.currCustomer.currAccount = currAccount
        if self.currCustomer.currAccount is None:
            currAccount = 0
            self.accountSelection()
        return

    def goodBye(self):
        print("Thank you for banking with the bank_of_nerds")

    def welcErr(self):
        """ Used to notify the customer they provided an invalid selection """
        """ at the welcome screen """
        print("Invalid Option")
        self.welcome()

    def actErr(self):
        """ Used to notify the customer they provided an invalid selection """
        """ at the accountActions screen """
        print("Invalid Action")
        self.accountActions()

    def valueValidation(self, string, type_):
        """ valueValidation takes in a string and handles error checking """
        """ that is needed amongst different user inputs to reduce """
        """ redundancy. The method accepts a string and type_ the type """
        """ is used to dynamically check the type of input the string """
        """ expects. valueValidation returns the valid string """
        # continue to loop until condition is met
        while True:
            try:
                # assign the string passed to the function to "input"
                userInput = type_(input(string))
            except ValueError:
                print("Please enter a number")
                continue
            except KeyboardInterrupt:
                os.system("clear")
                print("\nThank you for banking with us!")
                sys.exit()
            except EOFError:
                os.system("clear")
                print("\nThank you for banking with us!")
                sys.exit()
            if type_ == int:
                if userInput < 0:
                    print("Please enter a valid number")
                    continue
            return userInput

    def __str__(self):
        menuOptions = "A: New Customers\nB: Existing Customers\nC: Exit\n"\
                      "\tHow may we assist you? "
        return menuOptions
