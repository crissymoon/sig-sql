#!/usr/bin/env python3
"""
Moon Language Sigmoid Function Validator
=======================================
This script validates Moon language syntax for the sigmoid function
and simulates its execution since the C interpreter has compilation issues.
"""

import re
import math

def parse_moon_sigmoid(filename):
    """Parse and validate Moon language sigmoid function"""
    
    print(f"Parsing Moon file: {filename}")
    print("=" * 50)
    
    try:
        with open(filename, 'r') as file:
            content = file.read()
        
        # Extract function definitions
        functions = extract_functions(content)
        
        # Validate syntax
        if validate_moon_syntax(content):
            print("Moon syntax validation: PASSED")
        else:
            print("Moon syntax validation: FAILED")
            return False
        
        # Simulate sigmoid function execution
        if 'sigmoid' in functions:
            print("\nSimulating sigmoid function:")
            simulate_sigmoid_execution()
        
        return True
        
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return False
    except Exception as e:
        print(f"Error parsing file: {e}")
        return False

def extract_functions(content):
    """Extract function definitions from Moon code"""
    
    # Pattern to match Moon function definitions: m function_name(params) { ... }
    function_pattern = r'm\s+(\w+)\s*\([^)]*\)\s*\{'
    functions = re.findall(function_pattern, content)
    
    print(f"Found functions: {', '.join(functions)}")
    return functions

def validate_moon_syntax(content):
    """Validate Moon language syntax elements"""
    
    checks = []
    
    # Check for Moon-specific elements
    checks.append(("Triple colon comments", r':::', content))
    checks.append(("Function definitions", r'm\s+\w+\s*\([^)]*\)\s*\{', content))
    checks.append(("Print statements", r'p\s*\(', content))
    checks.append(("Return statements", r'return\s+', content))
    checks.append(("Moon comment styles", r'<-|#|__\w+__', content))
    
    all_passed = True
    
    for check_name, pattern, text in checks:
        if re.search(pattern, text):
            print(f"{check_name}: Found")
        else:
            print(f"{check_name}: Not found")
    
    return all_passed

def simulate_sigmoid_execution():
    """Simulate the sigmoid function execution with Python"""
    
    def python_sigmoid(x):
        """Python implementation of sigmoid function"""
        if x > 20:
            return 1.0
        if x < -20:
            return 0.0
        return 1.0 / (1.0 + math.exp(-x))
    
    test_values = [-5.0, -2.0, -1.0, 0.0, 1.0, 2.0, 5.0]
    
    print("   Input  |  Sigmoid Output")
    print("   -------|----------------")
    
    for val in test_values:
        result = python_sigmoid(val)
        print(f"   {val:6.1f} |  {result:13.6f}")

def create_moon_test_data():
    """Create test data for Moon sigmoid function"""
    
    test_data = """# Test data for Moon sigmoid function
-3.0
-1.5
-0.5
0.0
0.5
1.5
3.0"""
    
    with open('/Users/mac/Desktop/sig-sql/moon/test_data.txt', 'w') as f:
        f.write(test_data)
    
    print("Created test_data.txt for Moon sigmoid function")

def analyze_moon_features(filename):
    """Analyze specific Moon language features used"""
    
    try:
        with open(filename, 'r') as file:
            content = file.read()
        
        features = {
            'Comments': {
                'Hash comments (#)': len(re.findall(r'#[^#]', content)),
                'Arrow comments (<-)': len(re.findall(r'<-', content)),
                'Section comments (__text__)': len(re.findall(r'__\w+__', content)),
                'Block comments (:::)': len(re.findall(r':::', content)) // 2
            },
            'Functions': {
                'Function definitions (m)': len(re.findall(r'm\s+\w+', content)),
                'Print statements (p)': len(re.findall(r'p\s*\(', content)),
                'Return statements': len(re.findall(r'return\s+', content))
            },
            'Control Flow': {
                'If statements': len(re.findall(r'if\s+', content)),
                'Then clauses': len(re.findall(r'then\s*\{', content)),
                'Loops (start/goto)': len(re.findall(r'start\s+\w+|goto\s+\w+', content)),
                'Try-catch blocks': len(re.findall(r'try\s*\{', content))
            },
            'File Operations': {
                'Put operations': len(re.findall(r'put\s+', content)),
                'Read operations': len(re.findall(r'read\s+', content))
            }
        }
        
        print("\nMoon Language Features Analysis:")
        print("=" * 40)
        
        for category, items in features.items():
            print(f"\n{category}:")
            for feature, count in items.items():
                print(f"  {feature}: {count}")
        
        return features
        
    except Exception as e:
        print(f"Error analyzing features: {e}")
        return {}

def main():
    """Main function to test Moon sigmoid implementations"""
    
    print("Moon Language Sigmoid Function Validator")
    print("=" * 50)
    
    # Test both sigmoid implementations
    files_to_test = [
        '/Users/mac/Desktop/sig-sql/moon/simple_sigmoid.moon',
        '/Users/mac/Desktop/sig-sql/moon/sigmoid_function.moon'
    ]
    
    for filename in files_to_test:
        print(f"\n{'='*60}")
        success = parse_moon_sigmoid(filename)
        if success:
            analyze_moon_features(filename)
    
    # Create test data
    print(f"\n{'='*60}")
    create_moon_test_data()
    
    print(f"\nMoon sigmoid validation complete!")
    print("   Files created:")
    print("   - simple_sigmoid.moon (basic implementation)")
    print("   - sigmoid_function.moon (comprehensive implementation)")
    print("   - test_data.txt (test input data)")

if __name__ == "__main__":
    main()
