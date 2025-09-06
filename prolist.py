# Error proof list sorting module desinged by Crissy Deutsch
# Setup as module, from other files:
# from sort_list import any_sort
# result = any_sort([3, "apple", 1.5])
# This is a Example of SOLID + Clean principles in Python
# S - Single Responsibility Principle (each function does one thing)
# O - Open/Closed Principle (can extend without modifying existing code)
# L - Liskov Substitution Principle (functions work with any type of list-like input)
# I - Interface Segregation Principle (focused, specific functions)
# D - Dependency Inversion Principle (uses abstration, not concrete types)
# This is a common style for Financial, Banking or Medical Software Development
# This uses if __name__ == "__main__": to allow import without running code
import re
import sys

the_list = [x for x in range(10)]
the_list.extend(["apple", "banana", 15, "learn", "to", 5.0])

def any_sort(lst, preserve_types=True):
    # Input validation
    if not isinstance(lst, (list, tuple, set)):
        try:
            lst = list(lst)
        except TypeError:
            print("Error: Cannot convert input to list")
            return []
        except MemoryError:
            print("Error: Not enough memory to convert input to list")
            return []
    
    if not lst:
        return lst
    
    try:
        def natty_key(item):
            text = str(item)
            parts = re.split(r'(\d+)', text)
            return [int(part) if part.isdigit() else part.lower() for part in parts]
        
        # Create list of original_item, sort_key pairs
        keyed_items = [(item, natty_key(item)) for item in lst]
        
        # Sort by the key
        keyed_items.sort(key=lambda x: x[1])
        
        # Extract original items to preserve data types
        return [item[0] for item in keyed_items]
        
    except MemoryError:
        print("Error: Not enough memory to sort this list. Try with a smaller dataset.")
        return lst
    except RecursionError:
        print("Error: Maximum recursion depth exceeded. List may contain circular references.")
        return lst
    except KeyboardInterrupt:
        print("\nSorting interrupted by user (Ctrl+C)")
        return lst
    except OverflowError:
        print("Error: Numerical overflow occurred during sorting")
        return lst
    except SystemError:
        print("Error: Internal system error occurred")
        return lst
    except OSError as e:
        print(f"Error: Operating system error: {e}")
        return lst
    except UnicodeError as e:
        print(f"Error: Unicode encoding/decoding error: {e}")
        return lst
    except AttributeError as e:
        print(f"Error: Object attribute error: {e}")
        return lst
    except ValueError as e:
        print(f"Error: Invalid value encountered: {e}")
        return lst
    except TypeError as e:
        print(f"Error: Type-related error: {e}")
        return lst
    except Exception as e:
        print(f"Unexpected error during sorting: {type(e).__name__}: {e}")
        return lst

def any_sort_strings(lst):
    try:
        def natty_key(item):
            text = str(item)
            return [int(part) if part.isdigit() else part.lower() 
                   for part in re.split(r'(\d+)', text)]
        
        return sorted(lst, key=natty_key)
    except MemoryError:
        print("Error: Not enough memory to sort this list")
        return lst
    except RecursionError:
        print("Error: Maximum recursion depth exceeded")
        return lst
    except KeyboardInterrupt:
        print("\nSorting interrupted by user")
        return lst
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")
        return lst

def check_memory_usage(lst):
    try:
        # Each item + overhead
        estimated_size = len(lst) * sys.getsizeof(lst[0]) if lst else 0
        if estimated_size > 100_000_000:  # 100MB limiting
            print(f"Warning: Large list detected (~{estimated_size//1_000_000}MB). This may consume significant memory!")
            return False
        return True
    except:
        return True  # If we can't estimate, proceed

def safe_any_sort(lst, preserve_types=True, check_memory=True):
    if check_memory and not check_memory_usage(lst):
        response = input("Continue anyway? (y/n): ").lower().strip()
        if response != 'y':
            print("Operation cancelled by user")
            return lst
    
    return any_sort(lst, preserve_types)

def linear_search(lst, target):
    if not isinstance(lst, (list, tuple, set)):
        try:
            lst = list(lst)
        except (TypeError, MemoryError):
            return -1
    
    if not lst:
        return -1
    
    try:
        for i, item in enumerate(lst):
            if item == target:
                return i
        return -1
    except (MemoryError, KeyboardInterrupt, Exception):
        return -1

def binary_search(lst, target):
    if not isinstance(lst, (list, tuple)):
        try:
            lst = list(lst)
        except (TypeError, MemoryError):
            return -1
    
    if not lst:
        return -1
    
    try:
        sorted_lst = any_sort(lst, preserve_types=True)
        left, right = 0, len(sorted_lst) - 1
        
        while left <= right:
            mid = (left + right) // 2
            if sorted_lst[mid] == target:
                return lst.index(target)
            elif str(sorted_lst[mid]).lower() < str(target).lower():
                left = mid + 1
            else:
                right = mid - 1
        return -1
    except (MemoryError, RecursionError, KeyboardInterrupt, OverflowError, Exception):
        return -1

def hash_search(lst, target):
    if not isinstance(lst, (list, tuple, set)):
        try:
            lst = list(lst)
        except (TypeError, MemoryError):
            return -1
    
    if not lst:
        return -1
    
    try:
        hash_table = {}
        for i, item in enumerate(lst):
            key = str(item).lower() if not isinstance(item, (int, float)) else item
            if key not in hash_table:
                hash_table[key] = []
            hash_table[key].append(i)
        
        search_key = str(target).lower() if not isinstance(target, (int, float)) else target
        return hash_table.get(search_key, [-1])[0]
    except (MemoryError, KeyboardInterrupt, Exception):
        return -1

def jump_search(lst, target):
    if not isinstance(lst, (list, tuple)):
        try:
            lst = list(lst)
        except (TypeError, MemoryError):
            return -1
    
    if not lst:
        return -1
    
    try:
        sorted_lst = any_sort(lst, preserve_types=True)
        n = len(sorted_lst)
        step = int(n ** 0.5)
        prev = 0
        
        while prev < n and str(sorted_lst[min(step, n) - 1]).lower() < str(target).lower():
            prev = step
            step += int(n ** 0.5)
            if prev >= n:
                return -1
        
        while prev < min(step, n):
            if sorted_lst[prev] == target:
                return lst.index(target)
            prev += 1
        return -1
    except (MemoryError, RecursionError, KeyboardInterrupt, OverflowError, Exception):
        return -1

def find_all_occurrences(lst, target):
    if not isinstance(lst, (list, tuple, set)):
        try:
            lst = list(lst)
        except (TypeError, MemoryError):
            return []
    
    if not lst:
        return []
    
    try:
        indices = []
        for i, item in enumerate(lst):
            if item == target:
                indices.append(i)
        return indices
    except (MemoryError, KeyboardInterrupt, Exception):
        return []

def search_by_pattern(lst, pattern):
    if not isinstance(lst, (list, tuple, set)):
        try:
            lst = list(lst)
        except (TypeError, MemoryError):
            return []
    
    if not lst or not pattern:
        return []
    
    try:
        matches = []
        compiled_pattern = re.compile(str(pattern).lower())
        for i, item in enumerate(lst):
            if compiled_pattern.search(str(item).lower()):
                matches.append(i)
        return matches
    except (re.error, MemoryError, KeyboardInterrupt, Exception):
        return []

def search_by_type(lst, target_type):
    if not isinstance(lst, (list, tuple, set)):
        try:
            lst = list(lst)
        except (TypeError, MemoryError):
            return []
    
    if not lst:
        return []
    
    try:
        matches = []
        for i, item in enumerate(lst):
            if isinstance(item, target_type):
                matches.append(i)
        return matches
    except (MemoryError, KeyboardInterrupt, Exception):
        return []

def search_range(lst, min_val, max_val):
    if not isinstance(lst, (list, tuple, set)):
        try:
            lst = list(lst)
        except (TypeError, MemoryError):
            return []
    
    if not lst:
        return []
    
    try:
        matches = []
        for i, item in enumerate(lst):
            try:
                if isinstance(item, (int, float)) and min_val <= item <= max_val:
                    matches.append(i)
            except (TypeError, ValueError):
                continue
        return matches
    except (MemoryError, KeyboardInterrupt, Exception):
        return []

if __name__ == "__main__":
    print("Any sort with comprehensive error handling")
    print("-" * 50)
    
    test_lists = [
        [3, "apple", 1.5, "banana", 10, 2.7],
        ["item10", "item1", "item2", 1, 10, 2],
        [True, False, 0, 1, "true", "false"],
        [],
        [float('inf'), -float('inf'), float('nan'), 42],
        ["—", "café", "北京", "москва", "test"],
    ] # List with mixed types and special characters for testing
    
    for i, test_list in enumerate(test_lists, 1):
        print(f"\nTest {i}:")
        print(f"Original: {test_list}")
        print(f"Types:    {[type(x).__name__ for x in test_list]}")
        
        try:
            result = any_sort(test_list)
            print(f"Sorted:   {result}")
            print(f"Types:    {[type(x).__name__ for x in result]}")
        except Exception as e:
            print(f"Test failed with: {type(e).__name__}: {e}")
    
    print("\nSearch function tests:")
    print("-" * 30)
    
    test_search_list = [1, "apple", 3.14, "banana", 5, "apple", 7, "test"]
    print(f"Search list: {test_search_list}")
    
    try:
        print(f"Linear search for 'apple': {linear_search(test_search_list, 'apple')}")
        print(f"Binary search for 5: {binary_search(test_search_list, 5)}")
        print(f"Hash search for 'banana': {hash_search(test_search_list, 'banana')}")
        print(f"Jump search for 3.14: {jump_search(test_search_list, 3.14)}")
        print(f"All occurrences of 'apple': {find_all_occurrences(test_search_list, 'apple')}")
        print(f"Pattern search for 'app': {search_by_pattern(test_search_list, 'app')}")
        print(f"Search by type str: {search_by_type(test_search_list, str)}")
        print(f"Search range 1-5: {search_range(test_search_list, 1, 5)}")
    except Exception as e:
        print(f"Search test failed: {e}")
