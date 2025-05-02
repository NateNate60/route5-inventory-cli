import requests

from info import info
from process_scan import process_scan
import config

def buy (token: str) -> None:
    """
    Buy one or more products from the customer.

    Parameters
        token (str): The user's login token
    """

    cart = {}
    price_total = 0

    while True:
        barcode = input("\nScan a bar code or press enter if done: ")

        if barcode == "":
            break

        barcode, item_type = process_scan(barcode)
        
        if barcode in cart:
            cart[barcode]['quantity'] += 1
            price_total += cart[barcode]['acquired_price']
            print(cart[barcode]['description'])
            continue

        if len(barcode) == 12:
            # UPC, get info from server
            product_info = info(token, barcode, False)
            
            if len(product_info) == 0:
                # New product
                description = input(f"Enter description: ")
            else:
                description = product_info['description']
                print(f"Description: {description}")
            item_type = "sealed"
            condition = "sealed"
        else:
            
            if len(barcode) in (13, 9, 8, 10):
                # slab
                item_type = "slab"
            else:
                item_type = "card"
            description = input(f"Enter description: ")
            condition = input('Enter condition: ')
        
        while True:
            try:
                comps = float(input(f"Enter the price at which we would sell this (not the amount paid to customer): $"))
                comps = round(comps * 100)
                break
            except ValueError:
                print("Invalid price entered. Please enter a decimal number.")
        
        while True:
            try:
                price = float(input(f"Enter price paid or trade value given: $"))
                price = round(price * 100)
                break
            except ValueError:
                print("Invalid price entered. Please enter a decimal number.")
        
        cart[barcode] = {
            "description": description,
            "quantity": 1,
            "acquired_price": price,
            "condition": condition,
            "item_type": item_type,
            "sale_price": comps
        }
        price_total += price
    
    print('\n===============\n')

    for item in cart:
        print (f"{cart[item]['description']} {cart[item]['condition']}")
        print(f"{cart[item]['quantity']}x ${cart[item]['acquired_price'] / 100} = ${cart[item]['acquired_price'] * cart[item]['quantity'] / 100}\n")
        
    print(f"Total price to be paid to customer: ${price_total / 100}")

    acquired_from_name = input(f"Input customer name: ")
    acquired_from_contact = input(f"Input customer telephone or e-mail: ")


    submit = input("Submit purchase? (y/n) ")
    if "y" in submit or "Y" in submit:
        data = {
            'items': [{
                'id': barcode,
                'type': cart[barcode]['item_type'],
                'description': cart[barcode]['description'],
                'condition': cart[barcode]['condition'],
                'acquired_price': cart[barcode]['acquired_price'],
                'sale_price': cart[barcode]['sale_price'],
                'quantity': cart[barcode]['quantity']
            } for barcode in cart],
            'acquired_from_name': acquired_from_name,
            'acquired_from_contact': acquired_from_contact
        }

        response = requests.post(f"{config.SERVER_URL}/v1/inventory/add",
                                    json=data,
                                    headers={"Authorization": f"Bearer {token}"})
        
        if response.status_code == 200:
            print(f"\nTransaction ID:{response.json()['txid']}")
            print("PURCHASE SUCCESSFUL\n")
        else:
            print(f"An error occurred. Server returned non-successful status code {response.status_code}")
        return

                    
        
        
        

        
