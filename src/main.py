#!/usr/bin/python3

import getpass
import requests

from sell import sell
from info import info
from buy import buy
from update import update

def main ():
    print ("Welcome!")
    token = getpass.getpass("Paste your login token: ")

    while True:
        print("\n===== MAIN MENU =====\n"
              "Input your choice:\n"
              "1. SELL to customer\n"
              "2. BUY from customer\n"
              "3. UPDATE PRICES\n"
              "4. CONSIGN item from customer")
        choice = input("Input your choice or scan a bar code: ")

        if choice == "1":
            sell(token)
        if choice == "2":
            buy(token)
        if choice == "3":
            update(token)
        if len(choice) > 3:
            info(token, choice)

if __name__ == "__main__":
    main()