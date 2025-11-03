def filter_long_words(words, min_length):
    """
    Return list of words longer than min_length.
    """
    if not isinstance(min_length, int):
        raise TypeError("min_length must be an integer")
    
    result = []
    for word in words:
        if isinstance(word, str):
            if len(word) > min_length:
                result.append(word)
        else:
            print(f"Element '{word}' is not a string and will be ignored.")
    return result