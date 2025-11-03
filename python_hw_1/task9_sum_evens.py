def sum_even_numbers(start, end):
    """
    Calculate sum of all even numbers from start to end (inclusive).
    Use a loop and if statement.
    """
    total = 0
    for num in range(start, end + 1):
        if num % 2 == 0:
            total += num
    return total