import unittest
from calculator import divide

class ExtraTests(unittest.TestCase):
    def test_behavior(self):
        self.assertEqual(divide(7, 2), 3.5)
        self.assertEqual(divide(-7, 2), -3.5)
