class Solution:
    
    def lengthOfLongestSubstring(self, s: str) -> int:
        counter = {}
        
        currentMax = ""
        chars = []
        for i in s:
            if i in counter:
                
                counter = {}
                if len(currentMax) < len(chars):
                    currentMax = "".join(chars)
                chars = []
                chars.append(i)
               
                continue
            else:
                counter[i] = 1
                chars.append(i)
                if len(currentMax) < len(chars):
                    currentMax = "".join(chars)
                
        return len(currentMax)
    
    def lengthOfLongestSubstring_SlidingWindowDict(self, s: str) -> int:
        char_index = {}  # stores last seen position
        left = 0
        max_length = 0
        
        for right in range(len(s)):
            # If character seen before and is in current window
            if s[right] in char_index and char_index[s[right]] >= left:
                # Jump left pointer directly past the duplicate
                left = char_index[s[right]] + 1
            
            # Update character's position
            char_index[s[right]] = right
            
            # Track max length
            max_length = max(max_length, right - left + 1)
        
        return max_length
    
    def lengthOfLongestSubstring_SlidingWindowSet(self, s: str) -> int:
        char_set = set()
        left = 0
        max_length = 0
        
        for right in range(len(s)):
            while s[right] in char_set:
                char_set.remove(s[left])
                left += 1
            
            char_set.add(s[right])
            max_length = max(max_length, right - left + 1)
        
        return max_length
if __name__ == "__main__":
    sol = Solution()
    print(sol.lengthOfLongestSubstring("abcdefghijklmnopqrstuvwxyz"))
    
    