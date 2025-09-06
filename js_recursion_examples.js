/**
 * TypeScript Recursion Examples (JavaScript version for immediate execution)
 * ========================================================================
 * This is the same recursion examples but in JavaScript format
 */

// 1. Basic Factorial
function factorial(n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

// 2. Fibonacci Sequence
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// 3. Array Sum
function arraySum(arr) {
    if (arr.length === 0) return 0;
    return arr[0] + arraySum(arr.slice(1));
}

// 4. String Reversal
function reverseString(str) {
    if (str.length <= 1) return str;
    return str[str.length - 1] + reverseString(str.slice(0, -1));
}

// 5. Binary Tree Traversal
function inorderTraversal(node) {
    if (!node) return [];
    return [
        ...inorderTraversal(node.left),
        node.value,
        ...inorderTraversal(node.right)
    ];
}

// 6. Deep Object Cloning
function deepClone(obj) {
    if (obj === null || typeof obj !== 'object') return obj;
    
    if (obj instanceof Array) {
        return obj.map(item => deepClone(item));
    }
    
    const cloned = {};
    for (const key in obj) {
        if (obj.hasOwnProperty(key)) {
            cloned[key] = deepClone(obj[key]);
        }
    }
    return cloned;
}

// 7. Palindrome Checker
function isPalindrome(str) {
    const cleaned = str.replace(/\s+/g, '').toLowerCase();
    if (cleaned.length <= 1) return true;
    if (cleaned[0] !== cleaned[cleaned.length - 1]) return false;
    return isPalindrome(cleaned.slice(1, -1));
}

// 8. Power Function
function power(base, exponent) {
    if (exponent === 0) return 1;
    if (exponent < 0) return 1 / power(base, -exponent);
    return base * power(base, exponent - 1);
}

// 9. Directory Size Calculation
function calculateTotalSize(directory) {
    if (directory.type === 'file') {
        return directory.size || 0;
    }
    
    if (!directory.children) return 0;
    
    return directory.children.reduce((total, child) => {
        return total + calculateTotalSize(child);
    }, 0);
}

// 10. Merge Sort
function mergeSort(arr) {
    if (arr.length <= 1) return arr;
    
    const mid = Math.floor(arr.length / 2);
    const left = mergeSort(arr.slice(0, mid));
    const right = mergeSort(arr.slice(mid));
    
    return merge(left, right);
}

function merge(left, right) {
    const result = [];
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

// 11. Tail Recursion with Accumulator
function tailRecursiveSum(arr, accumulator = 0) {
    if (arr.length === 0) return accumulator;
    return tailRecursiveSum(arr.slice(1), accumulator + arr[0]);
}

// Demo Function
function demonstrateRecursion() {
    console.log('TypeScript/JavaScript Recursion Examples');
    console.log('========================================\n');
    
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
    const tree = {
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
    const fileSystem = {
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
    
    // 11. Tail Recursive Sum
    console.log('11. Tail Recursive Sum:');
    const largeArray = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    console.log(`tailRecursiveSum([1,2,3,4,5,6,7,8,9,10]) = ${tailRecursiveSum(largeArray)}\n`);
    
    console.log('All recursion examples completed successfully!');
}

// Run the demonstration
demonstrateRecursion();
