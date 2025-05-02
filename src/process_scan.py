def process_scan (barcode: str) -> tuple[str, str]:
    """
    Process a scanned QR code or bar code.

    If a slab's QR code or bar code is passed, this function returns
    the slab's serial number. Otherwise, it return exactly what is
    passed to it.

    Parameters
        barcode (str): A scanned bar code or QR code
    Return
        (str, str): A tuple of the processed bar code and the item's type.
    """
    if "cgccomics.com" in barcode:
        # CGC old label QR code
        barcode = barcode.split('/')[-2]
        item_type = "slab"
    elif "CGCCARDS.COM" in barcode:
        # CGC new label QR code
        barcode = barcode.split('/')[-3]
        item_type = "slab"
    elif "psacard.com" in barcode:
        # PSA QR code
        barcode = barcode.split('/')[-2]
    elif len(barcode) == 26:
        # CGC old label barcode
        barcode = barcode[-10:]
        item_type = "slab"
    elif len(barcode) == 12:
        # UPC scanned
        item_type = "sealed"
    elif barcode[0] == 'A':
        # Asset tag scanned
        item_type = 'card'
    else:
        item_type = 'unknown'
    return (barcode, item_type)