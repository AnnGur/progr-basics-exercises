import warnings

def calculate_stats(numbers):
    """
    Calculate min, max, and average from a list of numbers.
    Returns: dictionary with keys 'min', 'max', 'average'
    """
    for n in numbers:
        if not isinstance(n, (int, float)):
            raise TypeError("Input must be a number (int or float)")
    
    minimum = min(numbers)
    maximum = max(numbers)
    average = sum(numbers) / len(numbers)
    
    return {'min': minimum, 'max': maximum, 'average': average}