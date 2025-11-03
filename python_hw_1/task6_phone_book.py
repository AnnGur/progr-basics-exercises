def find_phone_number(phone_book, name):
    """
    Look up phone number by name.
    Returns phone number or "Not found" if name doesn't exist.
    """
    if not name:
        return "Warning: Name key is empty."
    return phone_book.get(name, "Not found")