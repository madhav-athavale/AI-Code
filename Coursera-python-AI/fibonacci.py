
def fibonacci(n):
    """
    Generate a list of the first 'n' Fibonacci numbers.

    The Fibonacci sequence is a series of numbers in which each number is the 
    sum of the two preceding ones, usually starting with 0 and 1. This function 
    generates a list of the first 'n' numbers in this sequence.

    Parameters:
    ----------
    n : int
        The number of Fibonacci numbers to generate. Must be a positive integer.

    Returns:
    -------
    list
        A list of the first 'n' Fibonacci numbers.

    Examples:
    --------
    >>> fibonacci(1)
    [0]

    >>> fibonacci(2)
    [0, 1]

    >>> fibonacci(10)
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    Edge cases:
    ----------
    fibonacci(0) will return an empty list since there are no Fibonacci numbers 
    to generate.

    Raises:
    ------
    ValueError: 
        If 'n' is not a positive integer.

    """
    if type(n) is not int or n < 0:
        raise ValueError("'n' must be a positive integer.")
    fib_seq = [0, 1]
    while len(fib_seq) < n:
        fib_seq.append(fib_seq[-1] + fib_seq[-2])
    return fib_seq[:n]



import unittest

class TestFibonacci(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(fibonacci(1), [0])
        self.assertEqual(fibonacci(2), [0, 1])
        self.assertEqual(fibonacci(10), [0, 1, 1, 2, 3, 5, 8, 13, 21, 34])

    def test_edge(self):
        self.assertEqual(fibonacci(0), [])

    def test_error(self):
        with self.assertRaises(ValueError):
            fibonacci(-1)
        with self.assertRaises(ValueError):
            fibonacci('ten')

    def test_various(self):
        self.assertEqual(fibonacci(3), [0, 1, 1])
        self.assertEqual(fibonacci(5), [0, 1, 1, 2, 3])

if __name__ == '__main__':
    unittest.main()