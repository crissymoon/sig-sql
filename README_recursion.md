# TypeScript Recursion Examples

This repository contains comprehensive recursion examples implemented in TypeScript with full type safety and also available in JavaScript for immediate execution.

## Files Created

1. **`typescript_recursion_examples.ts`** - Full TypeScript implementation with type annotations
2. **`js_recursion_examples.js`** - JavaScript version for immediate execution
3. **`package.json`** - Node.js package configuration with TypeScript dependencies
4. **`tsconfig.json`** - TypeScript compiler configuration

## Recursion Examples Included

### 1. Mathematical Recursion
- **Factorial**: Calculate factorial of a number
- **Fibonacci**: Generate Fibonacci sequence
- **Power Function**: Calculate base^exponent using recursion

### 2. Array Processing
- **Array Sum**: Sum all elements in an array recursively
- **Merge Sort**: Divide-and-conquer sorting algorithm

### 3. String Processing
- **String Reversal**: Reverse a string recursively
- **Palindrome Checker**: Check if a string is a palindrome

### 4. Tree/Data Structure Operations
- **Binary Tree Traversal**: Inorder traversal of binary trees
- **Generic Tree Processing**: Process tree nodes with custom functions
- **Directory Size Calculation**: Calculate total size of nested directory structures

### 5. Advanced Patterns
- **Deep Object Cloning**: Recursively clone nested objects and arrays
- **Tail Recursion**: Optimized recursion using accumulators

## How to Run

### Quick Start (JavaScript Version)
```bash
# Run immediately without any setup
node js_recursion_examples.js
```

### TypeScript Version (with full type checking)
```bash
# Install dependencies (one-time setup)
npm install

# Run TypeScript version directly
npx ts-node typescript_recursion_examples.ts

# Or compile to JavaScript first
npx tsc typescript_recursion_examples.ts
node typescript_recursion_examples.js
```

### Available NPM Scripts
```bash
npm run start          # Run JavaScript version
npm run start:ts       # Run TypeScript version with ts-node
npm run compile        # Compile TypeScript to JavaScript
npm run compile:watch  # Watch mode compilation
npm run build          # Build project
```

## Example Output

The examples demonstrate various recursion patterns and will output:

```
TypeScript Recursion Examples
============================

1. Factorial Examples:
factorial(5) = 120
factorial(0) = 1
factorial(7) = 5040

2. Fibonacci Examples:
fibonacci(0) = 0
fibonacci(1) = 1
fibonacci(8) = 21
fibonacci(10) = 55

3. Array Sum Examples:
arraySum([1, 2, 3, 4, 5]) = 15
arraySum([]) = 0
arraySum([10, -5, 15]) = 20

... (continued)
```

## Key Learning Points

### Recursion Fundamentals
- **Base Case**: Every recursive function needs a condition to stop
- **Recursive Case**: The function calls itself with modified parameters
- **Stack Management**: Understanding how recursive calls use the call stack

### TypeScript Benefits
- **Type Safety**: Interfaces and generics ensure type correctness
- **Better IDE Support**: IntelliSense and error detection
- **Documentation**: Type annotations serve as documentation

### Optimization Patterns
- **Tail Recursion**: Using accumulators to optimize recursive calls
- **Memoization**: Cache results to avoid redundant calculations (can be added)
- **Base Case Optimization**: Handle simple cases directly

## Advanced Features

### Generic Functions
The examples include generic TypeScript functions that work with any type:
```typescript
function processTreeNodes<T, R>(
    node: TreeNode<T> | undefined,
    processor: (value: T) => R
): R[]
```

### Interface Definitions
Type-safe interfaces for complex data structures:
```typescript
interface TreeNode<T> {
    value: T;
    left?: TreeNode<T>;
    right?: TreeNode<T>;
}

interface Directory {
    name: string;
    type: 'file' | 'folder';
    children?: Directory[];
    size?: number;
}
```

## Error Handling

The examples include proper error handling and edge cases:
- Empty arrays and strings
- Null/undefined values
- Negative numbers for mathematical functions
- Deep nesting limits

## Performance Considerations

- **Stack Overflow**: Be aware of recursion depth limits
- **Time Complexity**: Some algorithms like naive Fibonacci have exponential complexity
- **Memory Usage**: Each recursive call uses stack memory

## Next Steps

You can extend these examples by:
1. Adding memoization to optimize Fibonacci calculation
2. Implementing iterative versions for comparison
3. Adding more complex tree operations
4. Creating recursive parsers or expression evaluators
5. Implementing graph traversal algorithms

## Dependencies

- **TypeScript**: For type checking and compilation
- **ts-node**: For direct TypeScript execution
- **@types/node**: TypeScript definitions for Node.js

All examples work with modern JavaScript/TypeScript environments and follow best practices for recursion implementation.
