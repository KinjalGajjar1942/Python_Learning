import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Day6.sqlLite import *

class TestDay6(unittest.TestCase):
    def test_dummy(self):
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
