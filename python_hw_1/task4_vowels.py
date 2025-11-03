def count_vowels(text):
    """
    Count the number of vowels (a, e, i, o, u) in text.
    Case-insensitive.
    """
    vowels = 'aeiouAEIOU'
    count = sum(1 for char in text if char in vowels)
    return count