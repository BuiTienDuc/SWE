import unittest
from calculator import divide

class IssueTests(unittest.TestCase):
    def test_behavior(self):
        self.assertEqual(divide(10, 0), 0)
