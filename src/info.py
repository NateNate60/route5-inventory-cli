import requests

import config

def info (token: str, barcode: str, print_info: bool = True) -> dict :
    """
    Flow for getting info about a product

    Parameters
        token (str): The user's login token
        barcode (str): The item's bar code
        print_info (bool): Whether to print the info to the terminal
    Return
        (dict) a dictionary with the info about the item from the server
    """

    # Call /inventory
    response = requests.get(f"{config.SERVER_URL}/v1/inventory",
                               params={"id": barcode},
                               headers={"Authorization": f"Bearer {token}"})
    
    # 404 means not found in inventory
    if response.status_code == 404:
        print("Scanned bar code was not found in inventory")
        return {}
    
    data = response.json()

    if print_info:
        print(f"\n{data['description']} {data['condition']}")
        print(f"Price: ${data['sale_price'] / 100}")
        print(f"In stock: {data['quantity']}")

        if data['consignor_name'] != '':
            print(f"Consignor: {data['consignor_name']}\n"
                f"Contact: {data['consignor_contact']}")
    return data
