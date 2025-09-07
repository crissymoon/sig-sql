# Python Range Function Examples

# Basic range usage patterns
range(10)           # 0 to 9
range(1, 11)        # 1 to 10
range(1, 51)        # 1 to 50
range(0, 100, 5)    # 0 to 95 step 5

# Common for loop patterns with range
for i in range(50):
    pass

for number in range(1, 51):
    pass

for x in range(10, 0, -1):
    pass

# Range in list comprehensions
numbers = [i for i in range(1, 51)]
squares = [x**2 for x in range(1, 11)]
evens = [i for i in range(2, 21, 2)]

# Range with enumerate
items = ['a', 'b', 'c', 'd', 'e']
for i in range(len(items)):
    print(f"Index {i}: {items[i]}")

# Nested range loops
for i in range(1, 6):
    for j in range(1, 4):
        print(f"{i},{j}")

# Range with conditional
for num in range(1, 101):
    if num % 2 == 0:
        print(f"Even: {num}")
    else:
        print(f"Odd: {num}")

# Range for specific counts
for count in range(1, 51):
    print(f"Number {count} of 50")
