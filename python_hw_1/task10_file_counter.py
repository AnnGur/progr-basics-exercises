def count_words_in_file(filename):
    """
    Count total number of words in a file.
    Handle FileNotFoundError - return 0 if file doesn't exist.
    """
    try:
        with open(filename, 'r') as file:
            count = 0
            for line in file:
                count += len(line.split())
            return count
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found. Returnin 0.")
        return 0