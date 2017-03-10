#!/bin/usr/env python3


class Account:

    def __init__(self, product, balance):
        self.balance = balance
        self.product = product

    def withdraw(self, number):
        self.balance = self.balance-number

    def deposit(self, number):
        self.balance = self.balance+number

    def __str__(self):
        menuOptions = "A: Deposit\nB: Withdraw\nC: Main Menu"


class Customer:

    def __init__(self, name, age, idnum, bank):
        self.name = name
        self.age = age
        self.id = idnum
        self.numAccounts = 0
        self.accounts = {}
        self.bank = bank

    def listAccounts(self):
        accountView = "{0} : {1} {2}"
        for product, accounts in self.accounts.items():
            print(accountView.format(product, accounts.product,
                  accounts.balance))

    def listProducts(self):
        for product, accounts in self.accounts.items():
            print(product, "(", len(accounts), ")")


class Bank:
    clientId = 0

    def __init__(self):
        self.clients = {}
        self.teller = Teller(self)

    def newClient(self):
        name = input("What is your name? ")
        age = input("What is your age? ")
        newClient = Customer(name, age, self.clientId, self)
        self.clients.update({self.clientId: newClient})
        print("Your ID number is:", self.clientId)
        self.clientId += 1
        self.teller.currCustomer = newClient
        self.teller.selectProduct()

    def createAccount(self, product, balance):
        newAccount = Account(product, balance)
        self.teller.currCustomer.numAccounts += 1
        self.teller.currCustomer.accounts.update({customer.numAccounts: \
                                                 newAccount})
        self.teller.deposit()

    def listClients(self):
        accountList = "{0}: {1}"
        for idNums, customers in self.clients.items():
            print(accountList.format(idNums, customers.name))
        self.teller.selectCustomer()

class Teller:
    menuOptions = ["A: New Customers", "B: Check Account"]
    productDict = {1: "Savings", 2: "Checkings", 3: "Retirement"}
    actionDict = {1: "Deposit", 2: "Withdraw", 3: "Create Account",\
                  4: "Main Menu" }
                


    def __init__(self, bank):
        self.bank = bank
        self.options = {}
        self.options['A'] = bank.newClient
        self.options['B'] = bank.listClients
        self.currCustomer = 0

    def welcome(self):
        userInput = input(self.__str__())
        self.options.get(userInput)()

    def selectProduct(self):
        for key, value in Teller.productDict.items():
            print(key,":",value)
        productKey = int(input("What kind of account " \
                                "would you like to open? "))
        
        self.bank.createAccount(Teller.productDict.get(productKey),
                               customer, deposit)

    def accountActions(self):
        action = int(input("What would you like to do? "))
    
    def selectCustomer(self):   
        customerId = int(input("Which account would you like to access? "))
        customer = self.bank.clients.get(customerID)
        accountActions(customer)

    def deposit(self):
        deposit = float(input("How much would you like to deposit? "))
        self.currCustomer.deposit(deposit)
        self.accountActions(self)


    def __str__(self):
        menuOptions = """A: New Customers\nB: Check Accounts"""
        return menuOptions


def main():

    bank = Bank()
    bank.teller.welcome()



if __name__ == "__main__":
    main()
