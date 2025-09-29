import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Day4.fastAPIDemo import *

class TestDay4(unittest.TestCase):
    def test_dummy(self):
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
