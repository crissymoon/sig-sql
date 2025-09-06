// Sorting Algorithms
function quickSort(arr) {
    if (arr.length <= 1) return arr;
    const pivot = arr[Math.floor(arr.length / 2)];
    const left = arr.filter(x => x < pivot);
    const right = arr.filter(x => x > pivot);
    return [...quickSort(left), pivot, ...quickSort(right)];
}

function mergeSort(arr) {
    if (arr.length <= 1) return arr;
    const mid = Math.floor(arr.length / 2);
    const left = mergeSort(arr.slice(0, mid));
    const right = mergeSort(arr.slice(mid));
    return merge(left, right);
}

function bubbleSort(arr) {
    for (let i = 0; i < arr.length; i++) {
        for (let j = 0; j < arr.length - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
            }
        }
    }
    return arr;
}

// Search Algorithms
function binarySearch(arr, target) {
    let left = 0, right = arr.length - 1;
    while (left <= right) {
        const mid = Math.floor((left + right) / 2);
        if (arr[mid] === target) return mid;
        if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}

// Data Structures
class LinkedList {
    constructor() {
        this.head = null;
        this.size = 0;
    }
    
    add(data) {
        const node = { data, next: null };
        if (!this.head) {
            this.head = node;
        } else {
            let current = this.head;
            while (current.next) current = current.next;
            current.next = node;
        }
        this.size++;
    }
}

class Stack {
    constructor() {
        this.items = [];
    }
    
    push(item) { this.items.push(item); }
    pop() { return this.items.pop(); }
    peek() { return this.items[this.items.length - 1]; }
    isEmpty() { return this.items.length === 0; }
}

class Queue {
    constructor() {
        this.items = [];
    }
    
    enqueue(item) { this.items.push(item); }
    dequeue() { return this.items.shift(); }
    front() { return this.items[0]; }
    isEmpty() { return this.items.length === 0; }
}

// Graph Algorithms
function dijkstra(graph, start) {
    const distances = {};
    const visited = new Set();
    const queue = [[start, 0]];
    
    while (queue.length > 0) {
        const [node, dist] = queue.shift();
        if (visited.has(node)) continue;
        
        visited.add(node);
        distances[node] = dist;
        
        for (const neighbor of graph[node] || []) {
            if (!visited.has(neighbor.node)) {
                queue.push([neighbor.node, dist + neighbor.weight]);
            }
        }
    }
    return distances;
}

// Dynamic Programming
function fibonacci(n, memo = {}) {
    if (n in memo) return memo[n];
    if (n <= 2) return 1;
    memo[n] = fibonacci(n - 1, memo) + fibonacci(n - 2, memo);
    return memo[n];
}

function longestCommonSubsequence(text1, text2) {
    const dp = Array(text1.length + 1).fill().map(() => Array(text2.length + 1).fill(0));
    
    for (let i = 1; i <= text1.length; i++) {
        for (let j = 1; j <= text2.length; j++) {
            if (text1[i - 1] === text2[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }
    return dp[text1.length][text2.length];
}
