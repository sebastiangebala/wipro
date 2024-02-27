import unittest
from calculator import Calculator

class TestCalculator(unittest.TestCase):
    def test_calculate_mean(self):
        self.assertEqual(Calculator.calculate_mean([10, 20, 30]), 20)

    def test_calculate_median_odd(self):
        self.assertEqual(Calculator.calculate_median([1, 2, 3]), 2)

    def test_calculate_median_even(self):
        self.assertEqual(Calculator.calculate_median([1, 2, 3, 4]), 2.5)

    def test_sum_newest(self):
        self.assertEqual(Calculator.sum_newest([1, 2, 3, 4, 5], 3), 12)

if __name__ == '__main__':
    unittest.main()
