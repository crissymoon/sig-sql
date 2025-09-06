def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

def power(base, exponent):
    if exponent == 0:
        return 1
    if exponent == 1:
        return base
    return base * power(base, exponent - 1)

def reverse_string(s):
    if len(s) <= 1:
        return s
    return s[-1] + reverse_string(s[:-1])

def binary_search(arr, target, left=0, right=None):
    if right is None:
        right = len(arr) - 1
    
    if left > right:
        return -1
    
    mid = (left + right) // 2
    
    if arr[mid] == target:
        return mid
    elif arr[mid] > target:
        return binary_search(arr, target, left, mid - 1)
    else:
        return binary_search(arr, target, mid + 1, right)

def count_down(n):
    if n <= 0:
        print("Done!")
        return
    print(n)
    count_down(n - 1)

def sum_digits(n):
    if n < 10:
        return n
    return n % 10 + sum_digits(n // 10)

def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)

def tree_traversal(node):
    if node is None:
        return []
    
    result = [node.value]
    for child in node.children:
        result.extend(tree_traversal(child))
    return result

def hanoi_towers(n, source, destination, auxiliary):
    if n == 1:
        print(f"Move disk 1 from {source} to {destination}")
        return
    
    hanoi_towers(n - 1, source, auxiliary, destination)
    print(f"Move disk {n} from {source} to {destination}")
    hanoi_towers(n - 1, auxiliary, destination, source)

if __name__ == "__main__":
    print("Recursion Examples:")
    print(f"factorial(5) = {factorial(5)}")
    print(f"fibonacci(8) = {fibonacci(8)}")
    print(f"power(2, 4) = {power(2, 4)}")
    print(f"reverse_string('hello') = {reverse_string('hello')}")
    print(f"sum_digits(12345) = {sum_digits(12345)}")
    print(f"gcd(48, 18) = {gcd(48, 18)}")
    
    arr = [1, 3, 5, 7, 9, 11, 13, 15]
    print(f"binary_search([1,3,5,7,9,11,13,15], 7) = {binary_search(arr, 7)}")
    
    print("\nCountdown from 5:")
    count_down(5)
    
    print("\nHanoi Towers (3 disks):")
    hanoi_towers(3, "A", "C", "B")
