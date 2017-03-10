#!/bin/usr/env python3


class Account:

    def __init__(self):
        self.balance = 0.0

    def withdraw(self, number):
        self.balance = self.balance-number

    def deposit(self, number):
        self.balance = self.balance+number


class Customer:

    def __init__(self, name, age, idnum):
        self.name = name
        self.age = age
        self.id = idnum
        self.savings = []
        self.checkings = []
        self.k401 = []

    def newSavings(self, deposit):
        newAccount = Account()
        newAccount.deposit(deposit)
        self.savings.append(newAccount)

    def newCheckings(self, deposit):
        newAccount = Account()
        newAccount.deposit(deposit)
        self.checkings.append(newAccount)

    def newk401(self, deposit):
        newAccount = Account()
        newAccount.deposit(deposit)
        self.k401.append(newAccount)

    def listAccounts(self):
        accountNumber = 0
        if len(self.savings) != 0:
            print("Savings")
            for accounts in self.savings:
                print(accountNumber, ":", accounts.balance)
                accountNumber += 1
        accountNumber = 0
        if len(self.checkings) != 0:
            print("Checkings")
            for accounts in self.checkings:
                print(accountNumber, ":", accounts.balance)
                accountNumber += 1
        accountNumber = 0
        if len(self.k401) != 0:
            print("k401")
            for accounts in self.k401:
                print(accountNumber, ":", accounts.balance)
                accountNumber += 1


class Bank:
    clientId = 0

    def __init__(self):
        self.clients = {}

    def newClient(self):
        name = input("What is your name? ")
        age = input("What is your age? ")
        newClient = Customer(name, age, self.clientId)
        self.clients.update({self.clientId: newClient})
        print("Your ID number is:", self.clientId)
        self.clientId += 1

    def listClients(self):
        accountList = "{0}: {1}"
        for idNums, customers in self.clients.items():
            print(accountList.format(idNums, customers.name))


def main():

    newBank = Bank()
    newBank.newClient()
    newBank.newClient()
    newBank.newClient()
    newBank.newClient()
    newBank.listClients()


if __name__ == "__main__":
    main()
