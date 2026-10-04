import unittest
from calculator import divide

class RegressionTests(unittest.TestCase):
    def test_behavior(self):
        self.assertEqual(divide(10, 2), 5)
