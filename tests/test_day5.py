import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Day5.user_api import *

class TestDay5(unittest.TestCase):
    def test_dummy(self):
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
