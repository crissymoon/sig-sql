/**
 * Comprehensive TypeScript Recursion Examples
 * ==========================================
 * This file demonstrates various recursion patterns in TypeScript
 * with proper type annotations and examples
 */

// 1. Basic Factorial (Mathematical Recursion)
function factorial(n: number): number {
    // Base case
    if (n <= 1) {
        return 1;
    }
    // Recursive case
    return n * factorial(n - 1);
}

// 2. Fibonacci Sequence (Multiple Recursive Calls)
function fibonacci(n: number): number {
    if (n <= 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// 3. Array Sum (Array Processing)
function arraySum(arr: number[]): number {
    if (arr.length === 0) {
        return 0;
    }
    return arr[0] + arraySum(arr.slice(1));
}

// 4. String Reversal (String Processing)
function reverseString(str: string): string {
    if (str.length <= 1) {
        return str;
    }
    return str[str.length - 1] + reverseString(str.slice(0, -1));
}

// 5. Binary Tree Node Interface and Traversal
interface TreeNode<T> {
    value: T;
    left?: TreeNode<T>;
    right?: TreeNode<T>;
}

function inorderTraversal<T>(node: TreeNode<T> | undefined): T[] {
    if (!node) {
        return [];
    }
    return [
        ...inorderTraversal(node.left),
        node.value,
        ...inorderTraversal(node.right)
    ];
}

// 6. Deep Object Cloning (Object Processing)
type DeepCloneable = {
    [key: string]: any;
};

function deepClone<T>(obj: T): T {
    if (obj === null || typeof obj !== 'object') {
        return obj;
    }
    
    if (Array.isArray(obj)) {
        return obj.map(item => deepClone(item)) as unknown as T;
    }
    
    const cloned = {} as T;
    for (const key in obj) {
        if (obj.hasOwnProperty(key)) {
            (cloned as any)[key] = deepClone((obj as any)[key]);
        }
    }
    return cloned;
}

// 7. Palindrome Checker (String Analysis)
function isPalindrome(str: string): boolean {
    // Clean the string (remove spaces, convert to lowercase)
    const cleaned = str.replace(/\s+/g, '').toLowerCase();
    
    if (cleaned.length <= 1) {
        return true;
    }
    
    if (cleaned[0] !== cleaned[cleaned.length - 1]) {
        return false;
    }
    
    return isPalindrome(cleaned.slice(1, -1));
}

// 8. Power Function (Mathematical)
function power(base: number, exponent: number): number {
    if (exponent === 0) {
        return 1;
    }
    if (exponent < 0) {
        return 1 / power(base, -exponent);
    }
    return base * power(base, exponent - 1);
}

// 9. Directory-like Structure Processing
interface Directory {
    name: string;
    type: 'file' | 'folder';
    children?: Directory[];
    size?: number;
}

function calculateTotalSize(directory: Directory): number {
    if (directory.type === 'file') {
        return directory.size || 0;
    }
    
    if (!directory.children) {
        return 0;
    }
    
    return directory.children.reduce((total, child) => {
        return total + calculateTotalSize(child);
    }, 0);
}

// 10. Merge Sort (Divide and Conquer)
function mergeSort(arr: number[]): number[] {
    if (arr.length <= 1) {
        return arr;
    }
    
    const mid = Math.floor(arr.length / 2);
    const left = mergeSort(arr.slice(0, mid));
    const right = mergeSort(arr.slice(mid));
    
    return merge(left, right);
}

function merge(left: number[], right: number[]): number[] {
    const result: number[] = [];
    let leftIndex = 0;
    let rightIndex = 0;
    
    while (leftIndex < left.length && rightIndex < right.length) {
        if (left[leftIndex] <= right[rightIndex]) {
            result.push(left[leftIndex]);
            leftIndex++;
        } else {
            result.push(right[rightIndex]);
            rightIndex++;
        }
    }
    
    return result.concat(left.slice(leftIndex), right.slice(rightIndex));
}

// 11. Generic Tree Traversal with Custom Processing
function processTreeNodes<T, R>(
    node: TreeNode<T> | undefined,
    processor: (value: T) => R
): R[] {
    if (!node) {
        return [];
    }
    
    return [
        processor(node.value),
        ...processTreeNodes(node.left, processor),
        ...processTreeNodes(node.right, processor)
    ];
}

// 12. Tail Recursion Example (with accumulator)
function tailRecursiveSum(arr: number[], accumulator: number = 0): number {
    if (arr.length === 0) {
        return accumulator;
    }
    return tailRecursiveSum(arr.slice(1), accumulator + arr[0]);
}

// Demo Function to Test All Examples
function demonstrateRecursion(): void {
    console.log('TypeScript Recursion Examples');
    console.log('============================\n');
    
    // 1. Factorial
    console.log('1. Factorial Examples:');
    console.log(`factorial(5) = ${factorial(5)}`);
    console.log(`factorial(0) = ${factorial(0)}`);
    console.log(`factorial(7) = ${factorial(7)}\n`);
    
    // 2. Fibonacci
    console.log('2. Fibonacci Examples:');
    console.log(`fibonacci(0) = ${fibonacci(0)}`);
    console.log(`fibonacci(1) = ${fibonacci(1)}`);
    console.log(`fibonacci(8) = ${fibonacci(8)}`);
    console.log(`fibonacci(10) = ${fibonacci(10)}\n`);
    
    // 3. Array Sum
    console.log('3. Array Sum Examples:');
    const numbers = [1, 2, 3, 4, 5];
    console.log(`arraySum([1, 2, 3, 4, 5]) = ${arraySum(numbers)}`);
    console.log(`arraySum([]) = ${arraySum([])}`);
    console.log(`arraySum([10, -5, 15]) = ${arraySum([10, -5, 15])}\n`);
    
    // 4. String Reversal
    console.log('4. String Reversal Examples:');
    console.log(`reverseString("hello") = "${reverseString("hello")}"`);
    console.log(`reverseString("TypeScript") = "${reverseString("TypeScript")}"`);
    console.log(`reverseString("a") = "${reverseString("a")}"\n`);
    
    // 5. Binary Tree Traversal
    console.log('5. Binary Tree Traversal:');
    const tree: TreeNode<number> = {
        value: 4,
        left: {
            value: 2,
            left: { value: 1 },
            right: { value: 3 }
        },
        right: {
            value: 6,
            left: { value: 5 },
            right: { value: 7 }
        }
    };
    console.log(`Inorder traversal: [${inorderTraversal(tree).join(', ')}]\n`);
    
    // 6. Deep Clone
    console.log('6. Deep Clone Example:');
    const original = {
        name: "John",
        age: 30,
        hobbies: ["reading", "coding"],
        address: { city: "New York", zip: "10001" }
    };
    const cloned = deepClone(original);
    console.log('Original object cloned successfully');
    console.log(`Objects are different instances: ${original !== cloned}`);
    console.log(`Deep properties are different instances: ${original.address !== cloned.address}\n`);
    
    // 7. Palindrome
    console.log('7. Palindrome Examples:');
    console.log(`isPalindrome("racecar") = ${isPalindrome("racecar")}`);
    console.log(`isPalindrome("hello") = ${isPalindrome("hello")}`);
    console.log(`isPalindrome("A man a plan a canal Panama") = ${isPalindrome("A man a plan a canal Panama")}\n`);
    
    // 8. Power Function
    console.log('8. Power Function Examples:');
    console.log(`power(2, 3) = ${power(2, 3)}`);
    console.log(`power(5, 0) = ${power(5, 0)}`);
    console.log(`power(2, -2) = ${power(2, -2)}\n`);
    
    // 9. Directory Size Calculation
    console.log('9. Directory Size Calculation:');
    const fileSystem: Directory = {
        name: "root",
        type: "folder",
        children: [
            {
                name: "documents",
                type: "folder",
                children: [
                    { name: "file1.txt", type: "file", size: 100 },
                    { name: "file2.pdf", type: "file", size: 250 }
                ]
            },
            { name: "image.jpg", type: "file", size: 500 },
            {
                name: "projects",
                type: "folder",
                children: [
                    { name: "project1.ts", type: "file", size: 150 }
                ]
            }
        ]
    };
    console.log(`Total directory size: ${calculateTotalSize(fileSystem)} bytes\n`);
    
    // 10. Merge Sort
    console.log('10. Merge Sort Example:');
    const unsorted = [64, 34, 25, 12, 22, 11, 90];
    const sorted = mergeSort(unsorted);
    console.log(`Original: [${unsorted.join(', ')}]`);
    console.log(`Sorted: [${sorted.join(', ')}]\n`);
    
    // 11. Generic Tree Processing
    console.log('11. Generic Tree Processing:');
    const stringTree: TreeNode<string> = {
        value: "root",
        left: { value: "left" },
        right: { value: "right" }
    };
    const upperCaseValues = processTreeNodes(stringTree, (value: string) => value.toUpperCase());
    console.log(`Uppercase values: [${upperCaseValues.join(', ')}]\n`);
    
    // 12. Tail Recursive Sum
    console.log('12. Tail Recursive Sum:');
    const largeArray = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    console.log(`tailRecursiveSum([1,2,3,4,5,6,7,8,9,10]) = ${tailRecursiveSum(largeArray)}\n`);
    
    console.log('All recursion examples completed successfully!');
}

// Export functions for use in other modules
export {
    factorial,
    fibonacci,
    arraySum,
    reverseString,
    inorderTraversal,
    deepClone,
    isPalindrome,
    power,
    calculateTotalSize,
    mergeSort,
    processTreeNodes,
    tailRecursiveSum,
    demonstrateRecursion,
    TreeNode,
    Directory
};

// Run demonstration if this file is executed directly
if (require.main === module) {
    demonstrateRecursion();
}
