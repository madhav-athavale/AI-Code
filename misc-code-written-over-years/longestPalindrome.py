class Solution:
    def longestPalindrome(self, s: str) -> str:
        s = s.strip()
        if s == '':
            return None
        if len(s) < 2:
            return s
        ln = len(s)
        ln2 = ln//2
        forward =s 
        reverse = "".join(reversed(s))
        i = 0
        while i <=ln2:
           if forward == reverse:
                return forward
           reverse = reverse[1:]
           forward = forward[:ln-1-i]
           i = i + 1
        return None
        
    
    
def main():
    
    test_cases = [
        "sabcqbas",
        "babad",
        "cbbd",
        "  ",
        "a",
        "ac",
        "racecar"
    ]
    
    s= "racecar"
    s = "a"
    for s in test_cases:
        sol= Solution()
        ln = len(s)
        mx = 0
        ansString = ''
        for i in range(ln):
            ret = sol.longestPalindrome(s[i:])
            # print(s[i:])
        
            
            if ret != None and len(ret) > mx:
                mx = len(ret)
                ansString = ret 
        ansString = None if ret is None else ret
        print (s)
        print(ansString)
        
    
if __name__ == '__main__':
    main()
    
    

