import numpy as np

class TreeNode:
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None

def sorted_array_to_bst(nums: list[int]) -> TreeNode:
    if  len(nums) == 0:
        return None
    
    mid = len(nums) // 2
    root = TreeNode(nums[mid])
    root.left  = sorted_array_to_bst(nums[:mid])
    root.right = sorted_array_to_bst(nums[mid+1:])
    return root

def inorder(node, result=[]):
    if node:
        inorder(node.left, result)
        result.append(node.val)
        inorder(node.right, result)
    return result

def print_tree(node, level=0, prefix="Root: "):
    if node:
        print(" " * (level * 4) + prefix + str(node.val))
        if node.left or node.right:
            if node.left:
                print_tree(node.left,  level+1, "L── ")
            if node.right:
                print_tree(node.right, level+1, "R── ")

# ── Example ────────────────────────────────────────────────────────────────────

ary = np.random.choice(20,size=7,replace=False)
nums =np.sort(ary)
#nums = [1, 2, 3, 4, 5, 6, 7]
root = sorted_array_to_bst(nums)

print_tree(root)
print("\nInorder (should match original):", inorder(root, []))
# ```

# Output:
# ```
# Root: 4
#     L─ 2
#         L─ 1
#         R─ 3
#     R─ 6
#         L─ 5
#         R─ 7

#Inorder ("should match original"): [1, 2, 3, 4, 5, 6, 7]