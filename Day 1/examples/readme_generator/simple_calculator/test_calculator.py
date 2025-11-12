"""
Unit tests for the Calculator class.
"""

import unittest
from calculator import Calculator


class TestCalculator(unittest.TestCase):
    """Test cases for Calculator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.calc = Calculator()
    
    def test_add(self):
        """Test addition operation."""
        self.assertEqual(self.calc.add(2, 3), 5)
        self.assertEqual(self.calc.add(-1, 1), 0)
        self.assertEqual(self.calc.add(0, 0), 0)
    
    def test_subtract(self):
        """Test subtraction operation."""
        self.assertEqual(self.calc.subtract(5, 3), 2)
        self.assertEqual(self.calc.subtract(0, 5), -5)
    
    def test_multiply(self):
        """Test multiplication operation."""
        self.assertEqual(self.calc.multiply(3, 4), 12)
        self.assertEqual(self.calc.multiply(0, 100), 0)
    
    def test_divide(self):
        """Test division operation."""
        self.assertEqual(self.calc.divide(10, 2), 5)
        self.assertEqual(self.calc.divide(7, 2), 3.5)
    
    def test_divide_by_zero(self):
        """Test division by zero raises ValueError."""
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)
    
    def test_history(self):
        """Test calculation history."""
        self.calc.add(1, 2)
        self.calc.subtract(5, 3)
        history = self.calc.get_history()
        self.assertEqual(len(history), 2)
        self.assertIn("1.0 + 2.0 = 3.0", history)
    
    def test_clear_history(self):
        """Test clearing history."""
        self.calc.add(1, 1)
        self.calc.clear_history()
        self.assertEqual(len(self.calc.get_history()), 0)


if __name__ == "__main__":
    unittest.main()

