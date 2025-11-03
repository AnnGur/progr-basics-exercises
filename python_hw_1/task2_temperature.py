def celsius_to_fahrenheit(celsius):
    """
    Convert Celsius to Fahrenheit.
    Formula: (C × 9/5) + 32
    """
    if not isinstance(celsius, (int, float)):
        print("Input must be a number (int or float). Returning None.")
        return None
    
    fahrenheit = (celsius * 9/5) + 32
    return fahrenheit