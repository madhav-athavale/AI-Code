class Solution:
    
    romanDict= {1:'I', 5:'V', 10:'X', 50:'L', 100 :'C', 500:'D', 1000 :'M'}
    
    val_sym = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100,  "C"), (90,  "XC"), (50,  "L"), (40,  "XL"),
        (10,   "X"), (9,   "IX"), (5,   "V"), (4,   "IV"),
        (1,    "I")
    ]
    
    def intToRoman(self, num: int) -> str:
        for sym,val in self.val_sym:
            print(sym,val)
        
    def romanToInt(self, s: str) -> int:
        num = 194
        for i in str(num):
            print(i)
        
if __name__ == "__main__":
    sol = Solution()
    print(sol.intToRoman(1))