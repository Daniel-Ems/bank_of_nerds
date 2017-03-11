#!/bin/usr/env python3
import os
import time
import sys

from bank_information import Account
from bank_information import MoneyMarket
from bank_information import Customer
from bank_information import Bank
from bank_information import Teller


def main():

    bank = Bank()
    bank.teller.welcome()

if __name__ == "__main__":
    main()
