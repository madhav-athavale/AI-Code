
# test cases for balanced tree. From AI.

import unittest
import numpy as np

class TreeNode:
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None

def sorted_array_to_bst(nums) -> TreeNode:
    if nums is None or len(nums) == 0:
        return None
    mid = len(nums) // 2
    root = TreeNode(nums[mid])
    root.left  = sorted_array_to_bst(nums[:mid])
    root.right = sorted_array_to_bst(nums[mid+1:])
    return root

# ── Helpers ────────────────────────────────────────────────────────────────────
def inorder(node):
    """Returns inorder traversal as a list — should match original sorted array."""
    if not node:
        return []
    return inorder(node.left) + [node.val] + inorder(node.right)

def height(node):
    """Returns height of the tree."""
    if not node:
        return 0
    return 1 + max(height(node.left), height(node.right))

def is_balanced(node):
    """Returns True if tree is height-balanced at every node."""
    if not node:
        return True
    left_h  = height(node.left)
    right_h = height(node.right)
    if abs(left_h - right_h) > 1:
        return False
    return is_balanced(node.left) and is_balanced(node.right)

def is_bst(node, min_val=float('-inf'), max_val=float('inf')):
    """Returns True if tree satisfies BST property."""
    if not node:
        return True
    if not (min_val < node.val < max_val):
        return False
    return (is_bst(node.left,  min_val, node.val) and
            is_bst(node.right, node.val, max_val))

# ── Test Cases ─────────────────────────────────────────────────────────────────
class TestSortedArrayToBST(unittest.TestCase):

    # ── Edge cases ─────────────────────────────────────────────────────────────
    def test_none_input(self):
        self.assertIsNone(sorted_array_to_bst(None))

    def test_empty_list(self):
        self.assertIsNone(sorted_array_to_bst([]))

    def test_empty_numpy_array(self):
        self.assertIsNone(sorted_array_to_bst(np.array([])))

    def test_single_element(self):
        root = sorted_array_to_bst([42])
        self.assertEqual(root.val, 42)
        self.assertIsNone(root.left)
        self.assertIsNone(root.right)

    def test_two_elements(self):
        root = sorted_array_to_bst([1, 2])
        self.assertEqual(inorder(root), [1, 2])
        self.assertTrue(is_balanced(root))

    # ── Correctness ────────────────────────────────────────────────────────────
    def test_inorder_matches_input_odd(self):
        nums = [1, 2, 3, 4, 5, 6, 7]
        root = sorted_array_to_bst(nums)
        self.assertEqual(inorder(root), nums)

    def test_inorder_matches_input_even(self):
        nums = [1, 2, 3, 4, 5, 6]
        root = sorted_array_to_bst(nums)
        self.assertEqual(inorder(root), nums)

    def test_is_valid_bst(self):
        root = sorted_array_to_bst([1, 2, 3, 4, 5, 6, 7])
        self.assertTrue(is_bst(root))

    def test_is_balanced_odd(self):
        root = sorted_array_to_bst([1, 2, 3, 4, 5, 6, 7])
        self.assertTrue(is_balanced(root))

    def test_is_balanced_even(self):
        root = sorted_array_to_bst([1, 2, 3, 4, 5, 6])
        self.assertTrue(is_balanced(root))

    def test_negative_numbers(self):
        nums = [-7, -5, -3, -1, 0, 2, 4]
        root = sorted_array_to_bst(nums)
        self.assertEqual(inorder(root), nums)
        self.assertTrue(is_balanced(root))
        self.assertTrue(is_bst(root))

    def test_large_array(self):
        nums = list(range(1, 1001))
        root = sorted_array_to_bst(nums)
        self.assertEqual(inorder(root), nums)
        self.assertTrue(is_balanced(root))
        self.assertTrue(is_bst(root))

    # ── NumPy input ────────────────────────────────────────────────────────────
    def test_numpy_array(self):
        nums = np.array([1, 2, 3, 4, 5, 6, 7])
        root = sorted_array_to_bst(nums)
        self.assertEqual(inorder(root), [1, 2, 3, 4, 5, 6, 7])
        self.assertTrue(is_balanced(root))

    def test_numpy_negative(self):
        nums = np.array([-5, -3, -1, 0, 2, 4])
        root = sorted_array_to_bst(nums)
        self.assertEqual(inorder(root), [-5, -3, -1, 0, 2, 4])
        self.assertTrue(is_bst(root))

    # ── Height checks ──────────────────────────────────────────────────────────
    def test_height_7_elements(self):
        # 7 elements → height should be 3
        root = sorted_array_to_bst([1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(height(root), 3)

    def test_height_1_element(self):
        root = sorted_array_to_bst([1])
        self.assertEqual(height(root), 1)

    # ── Root value check ───────────────────────────────────────────────────────
    def test_root_is_middle_element(self):
        # odd length — root must be exact middle
        root = sorted_array_to_bst([1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(root.val, 4)

    def test_root_is_middle_element_even(self):
        # even length — root is upper-middle (index len//2)
        root = sorted_array_to_bst([1, 2, 3, 4, 5, 6])
        self.assertEqual(root.val, 4)


if __name__ == "__main__":
    unittest.main(verbosity=2)
