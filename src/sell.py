import requests
import sys

import config

def sell (token: str) -> None:
    """
    Flow for selling things to the customer

    Parameters
        token (str): The user's login token
    """
    barcode = " "
    cart = {}
    items = {}
    price = 0

    print("Scan bar codes to add them to the cart, then press return when finished.")
    print("If a mistake is made, continue scanning. It can be corrected at the end.")
    while True:
        barcode = input("Scan bar code or press return if finished: ")

        print()
        
        if barcode == "":
            break

        if barcode not in items:
            response = requests.get(f"{config.SERVER_URL}/v1/inventory", 
                                    params={'id': barcode}, 
                                    headers={"Authorization": f"Bearer {token}"})
            if response.status_code == 404:
                print("ERROR: Scanned bar code is not in inventory", file=sys.stderr)
                continue
            inventory_info = response.json()
            items[barcode] = inventory_info
        else:
            inventory_info = items[barcode]

        # Check if too many items are in the cart (more than available in inventory)
        quantity_needed = cart[barcode] + 1 if barcode in cart else 1
        if quantity_needed > inventory_info["quantity"]:
            print(f"ERROR: Only {inventory_info['quantity']} are in stock but {quantity_needed} were scanned", file=sys.stderr)
            continue
        
        # Set desired quantity
        cart[barcode] = quantity_needed

        price += inventory_info['sale_price']
        
        
        print(f"{inventory_info['description']} {inventory_info['condition']}")
        print('CONSIGNED\n' if inventory_info["consignor_name"] != '' else '', end="")
        print(f"Unit price: {inventory_info['sale_price'] / 100}\tCurrent total price: {price / 100}")
        print()

    print('===============')

    item_no = 0
    for item in cart.keys():
        item_price = items[item]["sale_price"]
        print(f"#{item_no}: {items[item]['description']} {items[item]['condition']}")
        print(f"{cart[item]}x {item_price / 100} each = {item_price * cart[item] / 100}")
        print()

    if price == 0:
        print("There are no items in this order.\n")
        return

    print(f"Calculated price: {price / 100}")
    print()
    item = None
    while item != "":
        item = input("Scan items that need to be REMOVED from this order, or press enter if finished: ")
        if item in cart:
            print(f"Removed {items[item]['description']}")
            if cart[item] == 1:
                cart.pop(item)
            else:
                cart[item] -= 1
        else:
            print("That item is not in the cart.")
    
    print('\n===============\n')

    item_no = 0
    for item in cart.keys():
        item_price = items[item]["sale_price"]
        print(f"#{item_no}: {items[item]['description']} {items[item]['condition']}")
        print(f"{cart[item]}x {item_price / 100} each = {item_price * cart[item] / 100}")
        print()

    print(f"Calculated price: {price / 100}")
    price_paid = 100*float(input("Input price paid by customer: "))

    discount = price_paid / price

    submit = input("Submit sale? (y/n) ")

    if "y" in submit or "Y" in submit:
        order_data = [
            {
                "id": item, 
                "sale_price": int(items[item]["sale_price"] * discount),
                "quantity": cart[item]
            } for item in cart
        ]
        response = requests.post(f"{config.SERVER_URL}/v1/inventory/remove",
                                 json=order_data,
                                 headers={"Authorization": f"Bearer {token}"})
        if response.status_code == 200:
            print(f"\nTransaction ID:{response.json()['txid']}")
            print('SALE SUCCESSFUL\n')
    print()
    return
            
        



            

            
        