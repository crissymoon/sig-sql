# Python For Loop Patterns - Basic Range Examples

# Simple counting loop
for i in range(1, 11):
    print(f"Count: {i}")

# Loop from 1 to 50
for number in range(1, 51):
    print(number)

# Loop with step
for i in range(1, 100, 2):
    print(f"Odd number: {i}")

# Loop from 0 to 10
for x in range(11):
    print(x)

# Loop from 5 to 15
for val in range(5, 16):
    print(f"Value: {val}")

# Countdown loop
for count in range(10, 0, -1):
    print(f"Countdown: {count}")

# Sum calculation with range
total = 0
for num in range(1, 101):
    total += num
print(f"Sum of 1-100: {total}")

# Print even numbers 1 to 20
for i in range(2, 21, 2):
    print(f"Even: {i}")

# Range with multiplication table
for i in range(1, 13):
    print(f"5 x {i} = {5 * i}")

# Basic iteration pattern
for item in range(1, 6):
    result = item * item
    print(f"Square of {item} = {result}")
