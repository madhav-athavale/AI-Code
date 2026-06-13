

def factorial(n):
    """ 
    Calculate the factorial of a number.

    This recursive function multiplies a given number 'n' successively by every positive integer less than 
    'n' until 1 is reached. If 'n' is 0, the function returns 1.

    Parameters:
    n (int): The integer of which the factorial is to be calculated.

    Return:
    int: The factorial of 'n'.

    Examples:
    >>> factorial(5) 
    25 

    >>> factorial(0)
    1

    Edge Cases:
    >>> factorial(-5)
    Throws exception because factorial is not defined for negative numbers.

    >>> factorial(1.0)
    Throws exception because factorial is only defined for integers.

    """
    
    if not isinstance(n, int) or n < 0:
        raise ValueError('Input must be a positive integer')
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)


import unittest

class TestFactorialFunction(unittest.TestCase):

    def test_basic(self):
        # Test basic cases
        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(6), 720)

    def test_edge_cases(self):
        # Test edge cases
        self.assertEqual(factorial(0), 1)

        # Case of negative numbers where the function should throw a value error
        with self.assertRaises(ValueError):
            factorial(-5)

        # Case for floating point numbers where the function should raise a value error
        with self.assertRaises(ValueError):
            factorial(3.4)
        
    def test_various_input_scenarios(self):
        # Test case with very big input value should not raise a recursion error.
        factorial(1000)

        # Tests if the returned factorial is an integer
        self.assertTrue(isinstance(factorial(4), int))

if __name__ == '__main__':
    unittest.main()