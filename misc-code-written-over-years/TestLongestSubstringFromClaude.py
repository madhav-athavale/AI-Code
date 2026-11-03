"""
Comprehensive Unit Tests for Longest Substring Without Repeating Characters
Tests all three approaches with various edge cases
"""

import unittest
import pytest
from LengthOfLongestSubstring import Solution


class TestLongestSubstring(unittest.TestCase):
    """Test suite for longest substring without repeating characters"""
    
    def setUp(self):
        """Initialize Solution object before each test"""
        self.sol = Solution()
    
    # ========================================================================
    # BASIC TEST CASES
    # ========================================================================
    
    def test_example1_abcabcbb(self):
        """Test: 'abcabcbb' should return 3 (substring: 'abc')"""
        s = "abcabcbb"
        expected = 3
        
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowSet(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowDict(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_Optimized(s), expected)
    
    def test_example2_pwwkew(self):
        """Test: 'pwwkew' should return 3 (substring: 'wke' or 'kew')"""
        s = "pwwkew"
        expected = 3
        
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowSet(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowDict(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_Optimized(s), expected)
    
    def test_example3_dvdf(self):
        """Test: 'dvdf' should return 3 (substring: 'vdf')"""
        s = "dvdf"
        expected = 3
        
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowSet(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowDict(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_Optimized(s), expected)
    
    # ========================================================================
    # EDGE CASES: Empty and Single Character
    # ========================================================================
    
    def test_empty_string(self):
        """Test: '' should return 0"""
        s = ""
        expected = 0
        
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowSet(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowDict(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_Optimized(s), expected)
    
    def test_single_character(self):
        """Test: 'a' should return 1"""
        s = "a"
        expected = 1
        
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowSet(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowDict(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_Optimized(s), expected)
    
    def test_two_different_characters(self):
        """Test: 'au' should return 2"""
        s = "au"
        expected = 2
        
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowSet(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowDict(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_Optimized(s), expected)
    
    # ========================================================================
    # ALL REPEATING CHARACTER
    # ========================================================================
    
    def test_all_same_character(self):
        """Test: 'bbbbb' should return 1"""
        s = "bbbbb"
        expected = 1
        
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowSet(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowDict(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_Optimized(s), expected)
    
    def test_long_same_character(self):
        """Test: 'aaaaaaa' should return 1"""
        s = "a" * 100
        expected = 1
        
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowSet(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowDict(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_Optimized(s), expected)
    
    # ========================================================================
    # ALL UNIQUE CHARACTERS
    # ========================================================================
    
    def test_all_unique(self):
        """Test: 'abcdefg' should return 7"""
        s = "abcdefg"
        expected = 7
        
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowSet(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowDict(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_Optimized(s), expected)
    
    def test_all_lowercase_letters(self):
        """Test: 'abcdefghijklmnopqrstuvwxyz' should return 26"""
        s = "abcdefghijklmnopqrstuvwxyz"
        expected = 26
        
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowSet(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowDict(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_Optimized(s), expected)
    
    # ========================================================================
    # REPEATING AT DIFFERENT POSITIONS
    # ========================================================================
    
    def test_repeat_at_beginning(self):
        """Test: 'aab' should return 2 (substring: 'ab')"""
        s = "aab"
        expected = 2
        
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowSet(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowDict(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_Optimized(s), expected)
    
    def test_repeat_at_end(self):
        """Test: 'abba' should return 2 (substring: 'ab' or 'ba')"""
        s = "abba"
        expected = 2
        
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowSet(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowDict(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_Optimized(s), expected)
    
    def test_repeat_in_middle(self):
        """Test: 'abcab' should return 3 (substring: 'cab')"""
        s = "abcab"
        expected = 3
        
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowSet(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowDict(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_Optimized(s), expected)
    
    # ========================================================================
    # SPECIAL CHARACTERS
    # ========================================================================
    
    def test_with_special_characters(self):
        """Test: 'aabaab!bb' should return 3 (substring: 'b!b')"""
        s = "aabaab!bb"
        expected = 3
        
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowSet(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowDict(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_Optimized(s), expected)
    
    def test_with_spaces(self):
        """Test: 'a b c a' should return 4 (substring: ' c a' or similar)"""
        s = "a b c a"
        expected = 4
        
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowSet(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowDict(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_Optimized(s), expected)
    
    def test_with_numbers(self):
        """Test: '123121' should return 3 (substring: '321')"""
        s = "123121"
        expected = 3
        
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowSet(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowDict(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_Optimized(s), expected)
    
    # ========================================================================
    # CASE SENSITIVITY
    # ========================================================================
    
    def test_case_sensitive(self):
        """Test: 'aA' should return 2 (case-sensitive)"""
        s = "aA"
        expected = 2
        
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowSet(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowDict(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_Optimized(s), expected)
    
    def test_mixed_case(self):
        """Test: 'AaBbCc' should return 6 (all characters different)"""
        s = "AaBbCc"
        expected = 6
        
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowSet(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowDict(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_Optimized(s), expected)
    
    # ========================================================================
    # LONG STRINGS
    # ========================================================================
    
    def test_long_unique_string(self):
        """Test: Long string with all unique characters"""
        s = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        expected = len(s)
        
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowSet(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowDict(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_Optimized(s), expected)
    
    def test_long_repeating_pattern(self):
        """Test: Long repeating pattern"""
        s = "abcdefg" * 100
        expected = 7  # Only 'abcdefg' is unique
        
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowSet(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowDict(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_Optimized(s), expected)
    
    def test_large_string_all_same(self):
        """Test: Very long string with same character"""
        s = "x" * 10000
        expected = 1
        
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowSet(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowDict(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_Optimized(s), expected)
    
    # ========================================================================
    # EDGE CASES: Duplicate at specific positions
    # ========================================================================
    
    def test_duplicate_immediately(self):
        """Test: 'aa' should return 1"""
        s = "aa"
        expected = 1
        
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowSet(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowDict(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_Optimized(s), expected)
    
    def test_duplicate_far_apart(self):
        """Test: 'abcdefg...a' - duplicate far apart"""
        s = "abcdefghijklmnopqrstuvwxyza"
        expected = 26  # 'abcdefghijklmnopqrstuvwxyz'
        
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowSet(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_SlidingWindowDict(s), expected)
        self.assertEqual(self.sol.lengthOfLongestSubstring_Optimized(s), expected)
    
    # ========================================================================
    # CONSISTENCY TESTS (All approaches match)
    # ========================================================================
    
    def test_consistency_across_methods(self):
        """Verify all three approaches give identical results"""
        test_cases = [
            "",
            "a",
            "au",
            "dvdf",
            "pwwkew",
            "abcabcbb",
            "bbbbb",
            "abcdefghijklmnopqrstuvwxyz",
            "aabaab!bb",
            "tmmzuxt",
            "!@#$%^&*()",
        ]
        
        for s in test_cases:
            result1 = self.sol.lengthOfLongestSubstring_SlidingWindowSet(s)
            result2 = self.sol.lengthOfLongestSubstring_SlidingWindowDict(s)
            result3 = self.sol.lengthOfLongestSubstring_Optimized(s)
            
            self.assertEqual(result1, result2, 
                           f"Set != Dict for '{s}'")
            self.assertEqual(result2, result3, 
                           f"Dict != Optimized for '{s}'")
    
    # ========================================================================
    # WITH SUBSTRING (Debugging)
    # ========================================================================
    
    def test_with_substring_basic(self):
        """Test WithSubstring method returns correct length and substring"""
        s = "abcabcbb"
        length, substring = self.sol.lengthOfLongestSubstring_WithSubstring(s)
        
        self.assertEqual(length, 3)
        self.assertEqual(len(substring), 3)
        self.assertTrue(all(c == substring[i] for i in range(len(substring))))  # No duplicates
    
    def test_with_substring_empty(self):
        """Test WithSubstring on empty string"""
        s = ""
        length, substring = self.sol.lengthOfLongestSubstring_WithSubstring(s)
        
        self.assertEqual(length, 0)
        self.assertEqual(substring, "")
    
    def test_with_substring_all_unique(self):
        """Test WithSubstring on all unique string"""
        s = "abcdef"
        length, substring = self.sol.lengthOfLongestSubstring_WithSubstring(s)
        
        self.assertEqual(length, 6)
        self.assertEqual(substring, "abcdef")


# ============================================================================
# PYTEST-STYLE PARAMETRIZED TESTS
# ============================================================================

@pytest.mark.parametrize("s,expected", [
    ("", 0),
    ("a", 1),
    ("au", 2),
    ("dvdf", 3),
    ("pwwkew", 3),
    ("abcabcbb", 3),
    ("bbbbb", 1),
    ("abcdefghijklmnopqrstuvwxyz", 26),
    ("aab", 2),
    ("aabaab!bb", 3),
    ("aA", 2),
    ("123121", 3),
    ("aa", 1),
])
def test_sliding_window_set(s, expected):
    """Parametrized test for SlidingWindowSet approach"""
    sol = Solution()
    assert sol.lengthOfLongestSubstring_SlidingWindowSet(s) == expected


@pytest.mark.parametrize("s,expected", [
    ("", 0),
    ("a", 1),
    ("au", 2),
    ("dvdf", 3),
    ("pwwkew", 3),
    ("abcabcbb", 3),
    ("bbbbb", 1),
    ("abcdefghijklmnopqrstuvwxyz", 26),
    ("aab", 2),
    ("aabaab!bb", 3),
    ("aA", 2),
    ("123121", 3),
    ("aa", 1),
])
def test_sliding_window_dict(s, expected):
    """Parametrized test for SlidingWindowDict approach"""
    sol = Solution()
    assert sol.lengthOfLongestSubstring_SlidingWindowDict(s) == expected


@pytest.mark.parametrize("s,expected", [
    ("", 0),
    ("a", 1),
    ("au", 2),
    ("dvdf", 3),
    ("pwwkew", 3),
    ("abcabcbb", 3),
    ("bbbbb", 1),
    ("abcdefghijklmnopqrstuvwxyz", 26),
    ("aab", 2),
    ("aabaab!bb", 3),
    ("aA", 2),
    ("123121", 3),
    ("aa", 1),
])
def test_optimized(s, expected):
    """Parametrized test for Optimized approach"""
    sol = Solution()
    assert sol.lengthOfLongestSubstring_Optimized(s) == expected


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("Running Unit Tests")
    print("=" * 70 + "\n")
    unittest.main(argv=[''], verbosity=2, exit=False)
    
    print("\n" + "=" * 70)
    print("To run pytest tests, execute:")
    print("pytest test_longest_substring.py -v")
    print("=" * 70)