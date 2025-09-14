def linear_search_ordered(lst, target):
    for index, value in enumerate(lst):
        if value == target:
            return index  # Return the position where it was found
    return -1  # Return -1 if not found

# Example usage:
numbers = [10, 20, 30, 40, 50]
print(linear_search_ordered(numbers, 30))  # Output: 2
print(linear_search_ordered(numbers, 100)) # Output: -1

def linear_search_unordered(lst, target):
    for index, value in enumerate(lst):
        if value == target:
            return index  # Found the target, return its position
    return -1  # Target not found

# Example with an unordered list
fruits = ["banana", "apple", "mango", "grape", "orange"]
print(linear_search_unordered(fruits, "mango"))   # Output: 2
print(linear_search_unordered(fruits, "cherry"))  # Output: -1

