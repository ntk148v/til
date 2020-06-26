# 9 top time complexities

Source: https://adrianmejia.com/most-popular-algorithms-time-complexity-every-programmer-should-know-free-online-tutorial-course/

- [9 top time complexities](#9-top-time-complexities)
  - [1. What is time complexity?](#1-what-is-time-complexity)
  - [2. O(1) - Constant time](#2-o1---constant-time)
  - [3. O(n) - Linear time](#3-on---linear-time)
  - [4. O(n^2) - Quadratic time](#4-on2---quadratic-time)
  - [5. O(n^c) - Polynomial time](#5-onc---polynomial-time)
  - [6. O(log n) - Logarithmic time](#6-olog-n---logarithmic-time)
  - [7. O(n log n) - Linearithmic](#7-on-log-n---linearithmic)
  - [8. O(2^n) - Exponential time](#8-o2n---exponential-time)
  - [9. O(n!) - Factorial time](#9-on---factorial-time)
  - [10. All running complexities graphs](#10-all-running-complexities-graphs)

## 1. What is time complexity?

- Time complexity estimates how algorithm performs regardless kind of machine it runs on.
- Time complexity is defined as a function of the input size `n` using Big-O notation, `n` indicates the size of the input, while O is the worst-case scenario growth rate function.
- [Big-O cheatsheet](https://www.bigocheatsheet.com)

## 2. O(1) - Constant time

- `O(1)` describes algorithms that take the same amount of time to compute regardless of the input size.
- Examples:
  - Find if a number is even or odd.
  - Check if an item on an array is null.
  - Print the first element from a list.
  - Find a value on a map.

## 3. O(n) - Linear time

- Linear running time algoriths are widespread. These algorithms imply that the program visits every element from the input.
- Examples:
  - Get the max/min value in a unsorted array.
  - Find a given element in a collection.
  - Print all the values in a list.

## 4. O(n^2) - Quadratic time

- A function with a quadratic time complexity has a growth rate of n^2. If the input size is 2, it will do 4 operations.
- Examples:
  - Check if a collection hash duplicated values.
  - Sorting items a collection using bubble sort, insertion sort, or selection sort.
  - Find all possible ordered pairs in an array.

## 5. O(n^c) - Polynomial time

- Polynomial running is represented as O(n^c), when c > 1. As you already saw, two inner loops almost translate to O(n^2) since it has to go through the array twice in most cases.

## 6. O(log n) - Logarithmic time

- Logarithmic time complexities usually apply to algorithms that divide problems in half every time.
- Examples: Binary Search!

## 7. O(n log n) - Linearithmic

- Linearithmic > Linear > Quadratic.
- Examples:
  - Efficient sorting algorithms like merge sort, quick sort and others.

## 8. O(2^n) - Exponential time

- Exponential (base 2) running time means that the calculations performed by an algorithm double every time as the input grows.
- Examples:
  - Fibonacci.
  - Power set: finding all subsets on a set.

## 9. O(n!) - Factorial time

- Factorial is the muliplication of all positive integer numbers less than itself.
- Examples:
  - Permutations of a string.

## 10. All running complexities graphs

![](https://adrianmejia.com/images/big-o-running-time-complexity.png)
