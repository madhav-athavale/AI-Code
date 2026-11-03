class Solution:
    def isPalindrome(self, x: int) -> bool:
        s = str(x)
        l = len(s)
        ln = l//2
        for i in range(ln):
            if s[i] == s[l -1 - i]:
                continue
            else:
                print("Not palindrome")
                return False
        return True
    
    def isPalindromeClaude(self, x: int) -> bool:
        if x < 0 or (x % 10 == 0 and x != 0):
            return False
        
        reversed_half = 0
        while x > reversed_half:
            reversed_half = reversed_half * 10 + x % 10
            x //= 10
        
        # Even length: x == reversed_half
        # Odd length:  x == reversed_half // 10 (middle digit doesn't matter)
        return x == reversed_half or x == reversed_half // 10
    
if __name__ == "__main__":
     sol = Solution()
     print(sol.isPalindromeClaude(12254))
            
        