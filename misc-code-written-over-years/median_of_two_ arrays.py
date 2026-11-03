
import math
class Solution:
    def findMedianSortedArrays(self, num1: List[int], num2: List[int]) -> float:
        ln1 = len(num1)
        ln2 = len(num2)
        ln = ln1 + ln2
        ind = 0
        median = 0
        i =0 
        j = 0
        
        mid1 = -math.inf
        mid2 = -math.inf
        while ind <ln //2 +1:
            if i < ln1 and j < ln2:
                if num1[i] <= num2[j]:
                    tmp = num1[i]
                    i +=1
                else:
                    tmp = num2[j]
                    j +=1
              
            if i < ln1 and j >=ln2:
                tmp = num1[i]
                
            if i >= ln1 and j < ln2:
                tmp = num2[j]
                      
            ind +=1
            
            mid1 = mid2
            mid2 = tmp
                
        if ln % 2  == 0:
            median = (mid1+mid2) / 2
        else:
            median =  mid2
        return median

if __name__ == "__main__":
    sol = Solution()
    ar1 = [1,3,11,15,17]
    ar2 = [2,6,8,9,16,18]
    print(sol.findMedianSortedArrays(ar1,ar2))
    
                