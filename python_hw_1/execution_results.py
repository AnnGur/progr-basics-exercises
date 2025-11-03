from task1_even_odd import check_even_odd
from task2_temperature import celsius_to_fahrenheit
from task3_list_stats import calculate_stats
from task4_vowels import count_vowels
from task5_filter_words import filter_long_words
from task6_phone_book import find_phone_number
from task7_grade import get_letter_grade
from task8_word_frequency import count_word_frequency
from task9_sum_evens import sum_even_numbers
from task10_file_counter import count_words_in_file

# python_hw_1/execution_results.py

## Task 1: Even or Odd
print('\n-----Task 1: Even or Odd-----\n')
print(check_even_odd(4))    # Even
print(check_even_odd(7))    # Odd 
print(check_even_odd(0))    # Even 
print(check_even_odd(-2.1)) # Odd

## Task 2: Convert Celsius to Fahrenheit
print('\n-----Task 2: Convert Celsius to Fahrenheit-----\n')
print(celsius_to_fahrenheit(0))       # 32.0
print(celsius_to_fahrenheit(100))     # 212.0
print(celsius_to_fahrenheit('100'))   # Input must be a number (int or float). Returning None.

## Task 3: Calculate min, max, and average from a list of numbers.
print('\n-----Task 3: Convert Celsius to Fahrenheit-----\n')
valid_result = calculate_stats([10, 20, 30, 40, 50])
print(valid_result)  # {'min': 10, 'max': 50, 'average': 30.0}
# invalid_result = calculate_stats([10.1, 20, 30, '40', 50])
# print(invalid_result)  # TypeError("Input must be a number (int or float)"). Commented, as it raises an exception and stops execution.

## Task 4: Count the number of vowels (a, e, i, o, u) in text.
print('\n-----Task 4: Convert Celsius to Fahrenheit-----\n')
print(count_vowels("Hello_World!")) # 3
print(count_vowels("Python 3"))     # 1

## Task 5: Return list of words longer than min_length.
print('\n-----Task 5: Return list of words longer than min_length.-----\n')
words = ["cat", "elephant", "dog", "butterfly"]
print(filter_long_words(words, 5))    # ["elephant", "butterfly"]
typesMix = ["hi", 123, "elephant", None, "bee"]
print(filter_long_words(typesMix, 3)) 
## Element '123' is not a string and will be ignored. 
## Element 'None' is not a string and will be ignored.
## ["elephant"]

## Task 6: Look up phone number by name.
print('\n-----Task 6: Look up phone number by name.-----\n')
phones = {"Alice": "123-456", "Bob": "789-012"}
print(find_phone_number(phones, "Alice"))   # "123-456"
print(find_phone_number(phones, "Charlie")) # "Not found"
print(find_phone_number(phones, "")) # Warning: Name key is empty.

## Task 7: Convert score to letter grade.
print('\n-----Task 7: Convert score to letter grade.-----\n')
print(get_letter_grade(95))  # "A"
print(get_letter_grade(82))  # "B"
print(get_letter_grade(55))  # "F"

## Task 8: Count frequency of each word in the list.
print('\n-----Task 8: Count frequency of each word in the list.-----\n')
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
print(count_word_frequency(words)) # {"apple": 3, "banana": 2, "cherry": 1}

## Task 9: Calculate sum of all even numbers from start to end (inclusive).
print('\n-----Task 9: Calculate sum of all even numbers from start to end (inclusive).-----\n')
print(sum_even_numbers(1, 10))   # 30 (2+4+6+8+10)
print(sum_even_numbers(5, 15))   # 50 (6+8+10+12+14)

## Task 10: Count total number of words in a file.
print('\n-----Task 10: Count total number of words in a file.-----\n')
# If file contains: "Hello world from Python"
print(count_words_in_file("resources/sample.txt"))  # 4
print(count_words_in_file("resources/empty.txt"))   # 0
print(count_words_in_file("resources/missing.txt")) # 0