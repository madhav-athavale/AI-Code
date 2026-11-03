"""
Comprehensive Unit Tests for Finding Median of 2 Sorted Arrays
Tests all three approaches with various edge cases and scenarios
"""

import unittest
import pytest
from typing import List
from median_sorted_arrays import Solution


class TestMedianSortedArrays(unittest.TestCase):
    """Test suite for median of 2 sorted arrays"""
    
    def setUp(self):
        """Initialize Solution object before each test"""
        self.sol = Solution()
    
    # ========================================================================
    # BASIC TEST CASES (From LeetCode)
    # ========================================================================
    
    def test_example1_even_length(self):
        """Test case: [1,3] and [2]"""
        ar1, ar2 = [1, 3], [2]
        expected = 2.0
        
        self.assertEqual(self.sol.findMedianSortedArrays_TwoPointer(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_BinarySearch(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_MergeSort(ar1, ar2), expected)
    
    def test_example2_even_length(self):
        """Test case: [1,2] and [3,4]"""
        ar1, ar2 = [1, 2], [3, 4]
        expected = 2.5
        
        self.assertEqual(self.sol.findMedianSortedArrays_TwoPointer(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_BinarySearch(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_MergeSort(ar1, ar2), expected)
    
    def test_example3_original(self):
        """Test case: [1,3,11,15,17] and [2,6,8,9,16]"""
        ar1, ar2 = [1, 3, 11, 15, 17], [2, 6, 8, 9, 16]
        expected = 8.5
        
        self.assertEqual(self.sol.findMedianSortedArrays_TwoPointer(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_BinarySearch(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_MergeSort(ar1, ar2), expected)
    
    # ========================================================================
    # EDGE CASES: Empty/Single Element Arrays
    # ========================================================================
    
    def test_empty_first_array(self):
        """Test case: [] and [1]"""
        ar1, ar2 = [], [1]
        expected = 1.0
        
        self.assertEqual(self.sol.findMedianSortedArrays_TwoPointer(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_BinarySearch(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_MergeSort(ar1, ar2), expected)
    
    def test_empty_second_array(self):
        """Test case: [2] and []"""
        ar1, ar2 = [2], []
        expected = 2.0
        
        self.assertEqual(self.sol.findMedianSortedArrays_TwoPointer(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_BinarySearch(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_MergeSort(ar1, ar2), expected)
    
    def test_both_single_element(self):
        """Test case: [1] and [2]"""
        ar1, ar2 = [1], [2]
        expected = 1.5
        
        self.assertEqual(self.sol.findMedianSortedArrays_TwoPointer(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_BinarySearch(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_MergeSort(ar1, ar2), expected)
    
    def test_large_empty_small_array(self):
        """Test case: [] and [1,2,3,4,5]"""
        ar1, ar2 = [], [1, 2, 3, 4, 5]
        expected = 3.0
        
        self.assertEqual(self.sol.findMedianSortedArrays_TwoPointer(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_BinarySearch(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_MergeSort(ar1, ar2), expected)
    
    # ========================================================================
    # ODD vs EVEN TOTAL LENGTH
    # ========================================================================
    
    def test_odd_total_length(self):
        """Test case with odd total length: [1,3] and [2]"""
        ar1, ar2 = [1, 3], [2]
        # Merged: [1, 2, 3] -> median is 2 (middle element)
        expected = 2.0
        
        self.assertEqual(self.sol.findMedianSortedArrays_TwoPointer(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_BinarySearch(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_MergeSort(ar1, ar2), expected)
    
    def test_even_total_length(self):
        """Test case with even total length: [1,2] and [3,4]"""
        ar1, ar2 = [1, 2], [3, 4]
        # Merged: [1, 2, 3, 4] -> median is (2 + 3) / 2 = 2.5
        expected = 2.5
        
        self.assertEqual(self.sol.findMedianSortedArrays_TwoPointer(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_BinarySearch(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_MergeSort(ar1, ar2), expected)
    
    # ========================================================================
    # DUPLICATE ELEMENTS
    # ========================================================================
    
    def test_all_same_elements(self):
        """Test case: [0,0] and [0,0]"""
        ar1, ar2 = [0, 0], [0, 0]
        expected = 0.0
        
        self.assertEqual(self.sol.findMedianSortedArrays_TwoPointer(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_BinarySearch(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_MergeSort(ar1, ar2), expected)
    
    def test_duplicate_elements_in_arrays(self):
        """Test case: [1,1,1] and [1,1,1]"""
        ar1, ar2 = [1, 1, 1], [1, 1, 1]
        expected = 1.0
        
        self.assertEqual(self.sol.findMedianSortedArrays_TwoPointer(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_BinarySearch(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_MergeSort(ar1, ar2), expected)
    
    def test_many_duplicates(self):
        """Test case: [1,2,2,2] and [2,2,3,4]"""
        ar1, ar2 = [1, 2, 2, 2], [2, 2, 3, 4]
        # Merged: [1, 2, 2, 2, 2, 2, 3, 4] -> median is (2 + 2) / 2 = 2.0
        expected = 2.0
        
        self.assertEqual(self.sol.findMedianSortedArrays_TwoPointer(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_BinarySearch(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_MergeSort(ar1, ar2), expected)
    
    # ========================================================================
    # NEGATIVE NUMBERS
    # ========================================================================
    
    def test_negative_numbers(self):
        """Test case: [-5,-3,-1] and [-4,-2,0]"""
        ar1, ar2 = [-5, -3, -1], [-4, -2, 0]
        # Merged: [-5, -4, -3, -2, -1, 0] -> median is (-3 + -2) / 2 = -2.5
        expected = -2.5
        
        self.assertEqual(self.sol.findMedianSortedArrays_TwoPointer(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_BinarySearch(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_MergeSort(ar1, ar2), expected)
    
    def test_mixed_positive_negative(self):
        """Test case: [-2, 3] and [1, 4]"""
        ar1, ar2 = [-2, 3], [1, 4]
        # Merged: [-2, 1, 3, 4] -> median is (1 + 3) / 2 = 2.0
        expected = 2.0
        
        self.assertEqual(self.sol.findMedianSortedArrays_TwoPointer(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_BinarySearch(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_MergeSort(ar1, ar2), expected)
    
    def test_all_negative(self):
        """Test case: [-10, -5] and [-8, -3]"""
        ar1, ar2 = [-10, -5], [-8, -3]
        # Merged: [-10, -8, -5, -3] -> median is (-8 + -5) / 2 = -6.5
        expected = -6.5
        
        self.assertEqual(self.sol.findMedianSortedArrays_TwoPointer(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_BinarySearch(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_MergeSort(ar1, ar2), expected)
    
    # ========================================================================
    # UNEQUAL ARRAY SIZES
    # ========================================================================
    
    def test_first_array_much_larger(self):
        """Test case: [1,2,3,4,5,6,7,8,9] and [10]"""
        ar1, ar2 = [1, 2, 3, 4, 5, 6, 7, 8, 9], [10]
        # Merged: [1,2,3,4,5,6,7,8,9,10] -> median is (5 + 6) / 2 = 5.5
        expected = 5.5
        
        self.assertEqual(self.sol.findMedianSortedArrays_TwoPointer(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_BinarySearch(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_MergeSort(ar1, ar2), expected)
    
    def test_second_array_much_larger(self):
        """Test case: [1] and [2,3,4,5,6,7,8,9,10]"""
        ar1, ar2 = [1], [2, 3, 4, 5, 6, 7, 8, 9, 10]
        # Merged: [1,2,3,4,5,6,7,8,9,10] -> median is (5 + 6) / 2 = 5.5
        expected = 5.5
        
        self.assertEqual(self.sol.findMedianSortedArrays_TwoPointer(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_BinarySearch(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_MergeSort(ar1, ar2), expected)
    
    # ========================================================================
    # LARGE NUMBERS
    # ========================================================================
    
    def test_large_numbers(self):
        """Test case: [1000000, 2000000] and [1500000]"""
        ar1, ar2 = [1000000, 2000000], [1500000]
        expected = 1500000.0
        
        self.assertEqual(self.sol.findMedianSortedArrays_TwoPointer(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_BinarySearch(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_MergeSort(ar1, ar2), expected)
    
    # ========================================================================
    # NON-OVERLAPPING ARRAYS
    # ========================================================================
    
    def test_no_overlap_first_smaller(self):
        """Test case: [1,2,3] and [4,5,6]"""
        ar1, ar2 = [1, 2, 3], [4, 5, 6]
        # Merged: [1,2,3,4,5,6] -> median is (3 + 4) / 2 = 3.5
        expected = 3.5
        
        self.assertEqual(self.sol.findMedianSortedArrays_TwoPointer(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_BinarySearch(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_MergeSort(ar1, ar2), expected)
    
    def test_no_overlap_second_smaller(self):
        """Test case: [4,5,6] and [1,2,3]"""
        ar1, ar2 = [4, 5, 6], [1, 2, 3]
        # Merged: [1,2,3,4,5,6] -> median is (3 + 4) / 2 = 3.5
        expected = 3.5
        
        self.assertEqual(self.sol.findMedianSortedArrays_TwoPointer(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_BinarySearch(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_MergeSort(ar1, ar2), expected)
    
    # ========================================================================
    # HEAVILY OVERLAPPING
    # ========================================================================
    
    def test_heavily_overlapping(self):
        """Test case: [1,5,9] and [2,3,4,6,7,8]"""
        ar1, ar2 = [1, 5, 9], [2, 3, 4, 6, 7, 8]
        # Merged: [1,2,3,4,5,6,7,8,9] -> median is 5
        expected = 5.0
        
        self.assertEqual(self.sol.findMedianSortedArrays_TwoPointer(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_BinarySearch(ar1, ar2), expected)
        self.assertEqual(self.sol.findMedianSortedArrays_MergeSort(ar1, ar2), expected)
    
    # ========================================================================
    # CONSISTENCY TESTS (All approaches give same result)
    # ========================================================================
    
    def test_consistency_across_all_methods(self):
        """Verify all three approaches give identical results"""
        test_cases = [
            ([1, 3], [2]),
            ([1, 2], [3, 4]),
            ([], [1]),
            ([1], []),
            ([1], [1]),
            ([-5, -3, -1], [-4, -2, 0]),
            ([1, 3, 11, 15, 17], [2, 6, 8, 9, 16]),
        ]
        
        for ar1, ar2 in test_cases:
            result1 = self.sol.findMedianSortedArrays_TwoPointer(ar1, ar2)
            result2 = self.sol.findMedianSortedArrays_BinarySearch(ar1, ar2)
            result3 = self.sol.findMedianSortedArrays_MergeSort(ar1, ar2)
            
            self.assertEqual(result1, result2, 
                           f"TwoPointer != BinarySearch for {ar1}, {ar2}")
            self.assertEqual(result2, result3, 
                           f"BinarySearch != MergeSort for {ar1}, {ar2}")
    
    # ========================================================================
    # FLOATING POINT PRECISION TESTS
    # ========================================================================
    
    def test_floating_point_precision(self):
        """Test floating point arithmetic is correct"""
        ar1, ar2 = [1, 3], [2]
        result = self.sol.findMedianSortedArrays_BinarySearch(ar1, ar2)
        self.assertAlmostEqual(result, 2.0, places=10)
    
    def test_floating_point_division(self):
        """Test correct division for even-length results"""
        ar1, ar2 = [1, 2], [3, 4]
        result = self.sol.findMedianSortedArrays_BinarySearch(ar1, ar2)
        self.assertAlmostEqual(result, 2.5, places=10)


# ============================================================================
# PYTEST-STYLE TESTS (Alternative)
# ============================================================================

@pytest.mark.parametrize("ar1,ar2,expected", [
    ([1, 3], [2], 2.0),
    ([1, 2], [3, 4], 2.5),
    ([], [1], 1.0),
    ([1], [], 1.0),
    ([1], [1], 1.0),
    ([-5, -3, -1], [-4, -2, 0], -2.5),
    ([0, 0], [0, 0], 0.0),
    ([1, 3, 11, 15, 17], [2, 6, 8, 9, 16], 8.5),
])
def test_median_binary_search(ar1, ar2, expected):
    """Parametrized test for BinarySearch approach"""
    sol = Solution()
    assert sol.findMedianSortedArrays_BinarySearch(ar1, ar2) == expected


@pytest.mark.parametrize("ar1,ar2,expected", [
    ([1, 3], [2], 2.0),
    ([1, 2], [3, 4], 2.5),
    ([], [1], 1.0),
    ([1], [], 1.0),
    ([1], [1], 1.0),
    ([-5, -3, -1], [-4, -2, 0], -2.5),
    ([0, 0], [0, 0], 0.0),
    ([1, 3, 11, 15, 17], [2, 6, 8, 9, 16], 8.5),
])
def test_median_two_pointer(ar1, ar2, expected):
    """Parametrized test for TwoPointer approach"""
    sol = Solution()
    assert sol.findMedianSortedArrays_TwoPointer(ar1, ar2) == expected


@pytest.mark.parametrize("ar1,ar2,expected", [
    ([1, 3], [2], 2.0),
    ([1, 2], [3, 4], 2.5),
    ([], [1], 1.0),
    ([1], [], 1.0),
    ([1], [1], 1.0),
    ([-5, -3, -1], [-4, -2, 0], -2.5),
    ([0, 0], [0, 0], 0.0),
    ([1, 3, 11, 15, 17], [2, 6, 8, 9, 16], 8.5),
])
def test_median_merge_sort(ar1, ar2, expected):
    """Parametrized test for MergeSort approach"""
    sol = Solution()
    assert sol.findMedianSortedArrays_MergeSort(ar1, ar2) == expected


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    # Run unittest tests
    print("=" * 70)
    print("Running Unit Tests")
    print("=" * 70)
    unittest.main(argv=[''], verbosity=2, exit=False)
    
    # Run pytest tests if available
    print("\n" + "=" * 70)
    print("To run pytest tests, execute:")
    print("pytest test_median_sorted_arrays.py -v")
    print("=" * 70)