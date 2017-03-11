#!/bin/usr/env python3
import os
import time

class Account:

    def __init__(self, product):
        self.balance = 0.0
        self.product = product

    def withdraw(self, withdraw):
        self.balance = self.balance-withdraw

    def deposit(self, deposit):
        self.balance = self.balance+deposit

    def __str__(self):
        menuOptions = "A: Deposit\nB: Withdraw\nC: Main Menu"


class Customer:

    def __init__(self, name, age, idnum):
        self.name = name
        self.age = age
        self.id = idnum
        self.numAccounts = 0
        self.accounts = {}
        self.currAccount = 0

    def listAccounts(self):
        accountList = []
        accountView = "{0} : {1} ${2}"
        for product, accounts in self.accounts.items():
            accountList.append(accountView.format(product, accounts.product,
                  accounts.balance))
        return accountList
        
    def listProducts(self):
        for product, accounts in self.accounts.items():
            print(product, "(", len(accounts), ")")

    def __str__(self):
        userView = "ID#{0}  Name: {1} Age: {2}  Accounts: {3}"
        return userView.format(self.id, self.name, self.age, self.numAccounts)


class Bank:
    clientId = 0

    def __init__(self):
        self.clients = {}
        self.teller = Teller(self)

    def newClient(self,name, age):  
        newClient = Customer(name, age, self.clientId)
        self.clients.update({self.clientId: newClient})
        self.clientId += 1
        self.teller.currCustomer = newClient
        self.teller.selectProduct()

    def createAccount(self, product):
        newAccount = Account(product)
        self.teller.currCustomer.currAccount = newAccount
        self.teller.currCustomer.numAccounts += 1
        accountId = self.teller.currCustomer.numAccounts
        self.teller.currCustomer.accounts.update({accountId: newAccount})
        self.teller.accountActions()

    def listClients(self):
        accountView = "{0}: {1}"
        customerList=[]
        for idNums, customers in self.clients.items():
            customerList.append(accountView.format(idNums, customers.name))
        return customerList

class Teller:
    productDict = {1: "Savings", 2: "Checkings", 3: "Retirement"}
    actionList = ["1: Deposit", "2: Withdraw", "3: Create Account", \
                  "4: List Accounts", "5: Main Menu" ]

    def __init__(self, bank):
        self.bank = bank
        self.currCustomer = Customer(0, 0, 0)
        self.options = {}
        self.options['a'] = self.newCustomer
        self.options['b'] = self.listCustomers
        self.options['c'] = self.goodBye
        self.actions = {}
        self.actions['1'] = self.deposit
        self.actions['2'] = self.withdraw
        self.actions['3'] = self.selectProduct
        self.actions['4'] = self.listAccounts
        self.actions['5'] = self.welcome

    def welcome(self):
        print("\tWelcome to the bank_of_nerds")
        userInput = input(self.__str__()).lower()
        self.options.get(userInput, self.invalidWelcome)()

    def newCustomer(self):
        name = input("What is your name? ")
        age = int(input("What is your age? "))
        self.bank.newClient(name, age)
        
    def selectProduct(self):
        os.system("clear")
        for key, value in Teller.productDict.items():
            print(key,":",value)
        productKey = int(input("What kind of account "\
                                "would you like to open? "))
        product = Teller.productDict.get(productKey, self.invalidProduct)
        if product == self.invalidProduct:
            self.invalidProduct()
        self.bank.createAccount(product)

    def accountActions(self):
        print(self.currCustomer.__str__())
        for items in Teller.actionList:
            print(items)
        action = input("What would you like to do? ")
        os.system("clear")
        self.actions.get(action, self.invalidAction)()
        
    def selectCustomer(self): 
        customerId = int(input("Which customer would you like to access? "))
        self.currCustomer = self.bank.clients.get(customerId, 
                                                    self.invalidCustomer)
        if self.currCustomer == self.invalidCustomer:
            self.invalidCustomer()
        os.system("clear")
        self.accountActions()

    def deposit(self):
        self.accountSelection()
        deposit = float(input("How much would you like to deposit? "))
        self.currCustomer.currAccount.deposit(deposit)
        os.system("clear")
        self.accountActions()

    def withdraw(self):
        self.accountSelection()
        if self.currCustomer.currAccount.product == "Retirement" and\
                                                    self.currCustomer.age < 67:
            os.system("clear")
            print("You are not old enough to pull from your retirement")
            self.accountActions()
        withdraw = float(input("How much would you like to withdraw? "))
        if (self.currCustomer.currAccount.balance - withdraw) < 0:
            os.system("clear")
            print("You do not have enough money to withdraw that amount")
            self.accountActions()
        self.currCustomer.currAccount.withdraw(withdraw)
        os.system("clear")
        self.accountActions()

    def listAccounts(self):
        accountList = self.currCustomer.listAccounts()
        for account in accountList:
            print(account)
        self.accountActions()

    def accountSelection(self):
        accountList = self.currCustomer.listAccounts()
        for item in accountList:
            print(item)
        account = int(input("Which account would you like to choose? "))
        self.currCustomer.currAccount = self.currCustomer.accounts.\
                                        get(account, self.invalidAccount)
        if self.currCustomer.currAccount == self.invalidAccount:
            self.invalidAccount()
        
        return

    def listCustomers(self):
        customerList = self.bank.listClients()
        if len(customerList) == 0:
            os.system("clear")
            print("\tWe have no customers yet")
            time.sleep(2)
            os.system("clear")
            self.welcome()
        else:
            for customer in customerList:
                print(customer)
            self.selectCustomer()

    def goodBye(self):
        print("Thank you for banking with the bank_of_nerds")
        
    def invalidSkeleton(self, string):
        os.system("clear")
        time.sleep(2)
        print(string)
        os.system("clear")
        return

    def invalidWelcome(self):
        self.invalidSkeleton("That is an invalid selection")
        self.welcome()

    def invalidCustomer(self):
        self.invalidSkeleton("That customer does not exist")
        self.listCustomers()

    def invalidProduct(self):
        self.invalidSkeleton("That product does not exist")
        self.selectProduct()

    def invalidAccount(self):
        self.invalidSkeleton("That account does not exist")
        self.accountSelection()

    def invalidAction(self):
        self.invalidSkeleton("That action does not exist")
        

    def __str__(self):
        menuOptions = "A: New Customers\nB: Existing Customers\nC: Exit\n"\
                      "\tHow may we assist you? "
        return menuOptions


def main():

    bank = Bank()
    bank.teller.welcome()



if __name__ == "__main__":
    main()
