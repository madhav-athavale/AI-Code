class Solution:
    def longestPalindrome(self, s: str) -> str:
        """
        Find the longest palindromic substring using expand-around-center approach.
        Time Complexity: O(n²)
        Space Complexity: O(1)
        """
        if not s or len(s) < 2:
            return s
        
        def expandAroundCenter(left: int, right: int) -> tuple:
            """Expand around center and return (start, end) of palindrome"""
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            # Return the valid palindrome indices
            return left + 1, right - 1
        
        start, end = 0, 0
        
        # Check all possible centers (both odd and even length palindromes)
        for i in range(len(s)):
            # Odd length palindromes (single character center)
            left1, right1 = expandAroundCenter(i, i)
            
            # Even length palindromes (two character center)
            left2, right2 = expandAroundCenter(i, i + 1)
            
            # Update if we found a longer palindrome
            if right1 - left1 > end - start:
                start, end = left1, right1
            
            if right2 - left2 > end - start:
                start, end = left2, right2
        
        return s[start:end + 1]


def main():
    test_cases = [
        "sabcqbas",
        "babad",
        "cbbd",
        "a",
        "ac",
        "racecar"
    ]
    
    sol = Solution()
    
    for s in test_cases:
        result = sol.longestPalindrome(s)
        print(f"Input: '{s}' -> Output: '{result}'")


if __name__ == '__main__':
    main()
