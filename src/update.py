import requests

import config
from process_scan import process_scan
from info import info
from convert_date import convert_date

def update (token: str) -> None:
    """
    Update the price of items
    """

    response = requests.get(f"{config.SERVER_URL}/v1/inventory/prices/stale", headers={"Authorization": f"Bearer {token}"})
    if response.status_code != 200:
        print(f"An error occurred. Server returned non-successful status code {response.status_code}")
        return
    stale_items = response.json()

    print("\nThe following items have stale prices (more than 1 week old) and should be updated:")
    
    for item in stale_items:
        print(f"{item['id']} {item['description']} {item['condition']}")
        print(f"Priced at ${item['sale_price'] / 100} on {convert_date(item['sale_price_date'])}\n")
    
    print()
    while True:
        barcode = input("Scan an item or enter its bar code to change its price, or press enter when done: ")

        if barcode == "":
            break

        barcode = process_scan(barcode)[0]

        info(token, barcode, True)

        while True:
            try:
                new_price = float(input("Enter new price: "))
                new_price = round(new_price * 100)
                break
            except ValueError:
                # Input wasn't a number
                print("Please enter a decimal number.")
        

        response = requests.patch(f"{config.SERVER_URL}/v1/inventory/prices",
                                  params={
                                      "id": barcode,
                                      "price": new_price
                                  },
                                  headers={"Authorization": f"Bearer {token}"})
        
        if response.status_code != 200:
            print(f"An error occurred. Server returned non-successful status code {response.status_code}")
        else:
            print("Update successful.\n")
