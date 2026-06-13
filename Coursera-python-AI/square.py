

def square_number(number):
    """
    This function squares the input number.

    Parameters:
    number (int, float): The number that needs to be squared.

    Returns:
    int, float: Returns the square of the input number.

    Examples:
    square_number(5) returns: 25
    square_number(2.0) returns: 4.0

    Edge Cases:
    square_number(0) returns: 0
    square_number(-2) returns: 4

    Note: This function does not handle complex numbers.
    """

    return number ** 2


import unittest

def square_number(number):
    """
    This function squares the input number.

    Parameters:
    number (int, float): The number that needs to be squared.

    Returns:
    int, float: Returns the square of the input number.

    Examples:
    square_number(5) returns: 25
    square_number(2.0) returns: 4.0

    Edge Cases:
    square_number(0) returns: 0
    square_number(-2) returns: 4

    Note: This function does not handle complex numbers.
    """

    return number ** 2

class TestSquareNumber(unittest.TestCase):

    def test_basic_functionality(self):
        self.assertEqual(square_number(5), 25)
        self.assertEqual(square_number(2.0), 4.0)

    def test_edge_cases(self):
        self.assertEqual(square_number(0), 0)
        self.assertEqual(square_number(-2), 4)

    def test_error_cases(self):
        with self.assertRaises(TypeError):
            square_number('a')
        with self.assertRaises(TypeError):
            square_number(None)

    def test_various_input_scenarios(self):
        self.assertEqual(square_number(1), 1)
        self.assertEqual(square_number(10), 100)
        self.assertEqual(square_number(1.1), 1.21)

if __name__ == '__main__':
    unittest.main()