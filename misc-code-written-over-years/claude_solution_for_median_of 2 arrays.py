"""
Finding median of 2 sorted arrays - Multiple approaches
"""

from typing import List
import math


class Solution:
    """
    APPROACH 1: Two-Pointer Merge (Fixed version of your code)
    Time Complexity: O(n + m)
    Space Complexity: O(1)
    """
    def findMedianSortedArrays_TwoPointer(self, num1: List[int], num2: List[int]) -> float:
        ln1 = len(num1)
        ln2 = len(num2)
        ln = ln1 + ln2
        
        i = 0  # pointer for num1
        j = 0  # pointer for num2
        
        mid1 = -math.inf  # first middle element
        mid2 = -math.inf  # second middle element
        
        # Iterate to the middle of merged array
        for ind in range(ln // 2 + 1):
            mid1 = mid2
            
            # Pick the smaller element from both arrays
            if i < ln1 and j < ln2:
                if num1[i] <= num2[j]:
                    mid2 = num1[i]
                    i += 1
                else:
                    mid2 = num2[j]
                    j += 1
            elif i < ln1:  # num2 exhausted
                mid2 = num1[i]
                i += 1
            else:  # num1 exhausted
                mid2 = num2[j]
                j += 1
        
        # If total length is even, return average of two middle elements
        if ln % 2 == 0:
            return (mid1 + mid2) / 2.0
        else:
            return mid2


    """
    APPROACH 2: Binary Search (OPTIMAL - Most Efficient)
    Time Complexity: O(log(min(m, n)))
    Space Complexity: O(1)
    
    KEY IDEA: Binary search on the partition point of the shorter array.
    We're looking for a partition where all left elements <= all right elements.
    """
    def findMedianSortedArrays_BinarySearch(self, num1: List[int], num2: List[int]) -> float:
        # Ensure num1 is the shorter array for efficiency
        if len(num1) > len(num2):
            return self.findMedianSortedArrays_BinarySearch(num2, num1)
        
        m, n = len(num1), len(num2)
        left, right = 0, m
        
        while left <= right:
            partition1 = (left + right) // 2
            partition2 = (m + n + 1) // 2 - partition1
            
            # Handle edge cases for partition boundaries
            left_max1 = -math.inf if partition1 == 0 else num1[partition1 - 1]
            right_min1 = math.inf if partition1 == m else num1[partition1]
            
            left_max2 = -math.inf if partition2 == 0 else num2[partition2 - 1]
            right_min2 = math.inf if partition2 == n else num2[partition2]
            
            # Check if we found the correct partition
            if left_max1 <= right_min2 and left_max2 <= right_min1:
                # Calculate median based on total length
                if (m + n) % 2 == 0:
                    return (max(left_max1, left_max2) + min(right_min1, right_min2)) / 2.0
                else:
                    return float(max(left_max1, left_max2))
            
            # Move partition
            elif left_max1 > right_min2:
                right = partition1 - 1
            else:
                left = partition1 + 1
        
        return -1.0  # Should never reach here for valid input


    """
    APPROACH 3: Merge and Sort (Simplest but Least Efficient)
    Time Complexity: O((m + n) log(m + n))
    Space Complexity: O(m + n)
    """
    def findMedianSortedArrays_MergeSort(self, num1: List[int], num2: List[int]) -> float:
        merged = sorted(num1 + num2)
        n = len(merged)
        
        if n % 2 == 0:
            return (merged[n // 2 - 1] + merged[n // 2]) / 2.0
        else:
            return float(merged[n // 2])


# ============================================================================
# PERFORMANCE COMPARISON
# ============================================================================

def benchmark():
    """Compare performance of all three approaches"""
    import time
    
    sol = Solution()
    
    # Test case 1: Small arrays
    ar1 = [1, 3, 11, 15, 17]
    ar2 = [2, 6, 8, 9, 16]
    
    print("=" * 70)
    print("TEST CASE 1: Small Arrays")
    print(f"Array 1: {ar1}")
    print(f"Array 2: {ar2}")
    print("=" * 70)
    
    # Two-Pointer
    start = time.perf_counter()
    result1 = sol.findMedianSortedArrays_TwoPointer(ar1, ar2)
    time1 = time.perf_counter() - start
    print(f"Two-Pointer: {result1:.2f} | Time: {time1*1e6:.2f}µs")
    
    # Binary Search
    start = time.perf_counter()
    result2 = sol.findMedianSortedArrays_BinarySearch(ar1, ar2)
    time2 = time.perf_counter() - start
    print(f"Binary Search: {result2:.2f} | Time: {time2*1e6:.2f}µs")
    
    # Merge & Sort
    start = time.perf_counter()
    result3 = sol.findMedianSortedArrays_MergeSort(ar1, ar2)
    time3 = time.perf_counter() - start
    print(f"Merge & Sort: {result3:.2f} | Time: {time3*1e6:.2f}µs")
    
    print(f"\n✓ All approaches return same result: {result1 == result2 == result3}")
    
    # Test case 2: Large arrays (where binary search shines)
    print("\n" + "=" * 70)
    print("TEST CASE 2: Large Arrays (10,000 elements each)")
    print("=" * 70)
    
    large1 = list(range(0, 20000, 2))  # 10,000 even numbers
    large2 = list(range(1, 20000, 2))  # 10,000 odd numbers
    
    # Two-Pointer
    start = time.perf_counter()
    result1 = sol.findMedianSortedArrays_TwoPointer(large1, large2)
    time1 = time.perf_counter() - start
    print(f"Two-Pointer: {result1:.2f} | Time: {time1*1e3:.2f}ms")
    
    # Binary Search (much faster!)
    start = time.perf_counter()
    result2 = sol.findMedianSortedArrays_BinarySearch(large1, large2)
    time2 = time.perf_counter() - start
    print(f"Binary Search: {result2:.2f} | Time: {time2*1e3:.2f}ms ⭐ {time1/time2:.0f}x faster!")
    
    # Merge & Sort
    start = time.perf_counter()
    result3 = sol.findMedianSortedArrays_MergeSort(large1, large2)
    time3 = time.perf_counter() - start
    print(f"Merge & Sort: {result3:.2f} | Time: {time3*1e3:.2f}ms")
    
    print(f"\n✓ All approaches return same result: {result1 == result2 == result3}")


# ============================================================================
# COMPLEXITY COMPARISON
# ============================================================================

print("\n" + "=" * 70)
print("COMPLEXITY ANALYSIS")
print("=" * 70)
print("""
┌─────────────────────────────────────────────────────────────┐
│ Approach          │ Time Complexity    │ Space Complexity   │
├─────────────────────────────────────────────────────────────┤
│ Two-Pointer       │ O(n + m)           │ O(1)               │
│ Binary Search ⭐  │ O(log(min(m,n)))   │ O(1)               │
│ Merge & Sort      │ O((n+m)log(n+m))   │ O(n + m)           │
└─────────────────────────────────────────────────────────────┘

RECOMMENDATION: Use Binary Search for interviews & production code.
It's the most efficient and impresses interviewers the most!
""")

# ============================================================================
# TESTS
# ============================================================================

if __name__ == "__main__":
    sol = Solution()
    
    print("\n" + "=" * 70)
    print("UNIT TESTS")
    print("=" * 70)
    
    # Test 1
    print("\nTest 1: [1,3] and [2]")
    ar1, ar2 = [1, 3], [2]
    result = sol.findMedianSortedArrays_BinarySearch(ar1, ar2)
    print(f"Result: {result} (Expected: 2.0) {'✓' if result == 2.0 else '✗'}")
    
    # Test 2
    print("\nTest 2: [1,2] and [3,4]")
    ar1, ar2 = [1, 2], [3, 4]
    result = sol.findMedianSortedArrays_BinarySearch(ar1, ar2)
    print(f"Result: {result} (Expected: 2.5) {'✓' if result == 2.5 else '✗'}")
    
    # Test 3
    print("\nTest 3: [1,3,11,15,17] and [2,6,8,9,16]")
    ar1, ar2 = [1, 3, 11, 15, 17], [2, 6, 8, 9, 16]
    result = sol.findMedianSortedArrays_BinarySearch(ar1, ar2)
    print(f"Result: {result} (Expected: 8.5) {'✓' if result == 8.5 else '✗'}")
    
    # Test 4: Uneven split
    print("\nTest 4: [0,0] and [0,0]")
    ar1, ar2 = [0, 0], [0, 0]
    result = sol.findMedianSortedArrays_BinarySearch(ar1, ar2)
    print(f"Result: {result} (Expected: 0.0) {'✓' if result == 0.0 else '✗'}")
    
    # Run benchmarks
    print("\n")
    benchmark()