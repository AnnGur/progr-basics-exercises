def count_word_frequency(words):
    """
    Count frequency of each word in the list.
    Returns: dictionary with word as key and count as value
    """
    frequency = {}
    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
    return frequency