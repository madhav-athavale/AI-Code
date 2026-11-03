import unittest

class Solution:
    def resultArray(self, nums: list[int]) -> list[int]:
        if not nums:
            return []
        if len(nums) == 1:
            return [nums[0]]
            
        lst1 = []
        lst2 = []
        lst1.append(nums[0])
        lst2.append(nums[1])
        for nxt in range(2,len(nums)):
            if nums[nxt] > lst1[len(lst1)- 1]:
                lst2.append(nums[nxt])
            else:
                
                lst1.append(nums[nxt])
            
        lst = lst1 + lst2
        #print(lst)
        return lst
           
def main():
    num = [3, 4, 5, 1, 7, -1, 9]
    
    sl = Solution()
    print(sl.resultArray(num)) 
       
        
        
if __name__ == '__main__':
    main()
    
    
# class TestSolutionUnittest(unittest.TestCase):
#     def setUp(self):
#         self.sol = Solution()

#     def test_basic_example(self):
#         self.assertEqual(
#             self.sol.resultArray([3, 4, 5, 1, 7, -1, 9]), 
#             [3, 5, 1, -1, 4, 7, 9]
#         )

#     def test_minimum_length(self):
#         self.assertEqual(self.sol.resultArray([10, 20]), [10, 20])

#     def test_all_greater(self):
#         self.assertEqual(self.sol.resultArray([1, 2, 5, 6]), [1, 2, 5, 6])

#     def test_all_smaller_or_equal(self):
#         self.assertEqual(self.sol.resultArray([5, 10, 4, 3, 5]), [5, 4, 3, 5, 10])

#     def test_mixed_negatives(self):
#         self.assertEqual(self.sol.resultArray([-3, -1, 0, 2, -5]), [-3, -5, -1, 0, 2])

#     def test_duplicates(self):
#         self.assertEqual(self.sol.resultArray([2, 2, 2, 2]), [2, 2, 2, 2])

# if __name__ == '__main__':
#     unittest.main()

# @pytest.mark.parametrize("nums, expected", [
#     ([3, 4, 5, 1, 7, -1, 9], [3, 5, 1, -1, 4, 7, 9]), # Basic example
#     ([10, 20], [10, 20]),                            # Minimum length
#     ([1, 2, 5, 6], [1, 2, 5, 6]),                    # All greater
#     ([5, 10, 4, 3, 5], [5, 4, 3, 5, 10]),            # All smaller/equal
#     ([-3, -1, 0, 2, -5], [-3, -5, -1, 0, 2]),        # Mixed negatives
#     ([2, 2, 2, 2], [2, 2, 2, 2])                     # Duplicates
# ])
# def test_result_array(nums, expected):
#     sol = Solution()
#     assert sol.resultArray(nums) == expected