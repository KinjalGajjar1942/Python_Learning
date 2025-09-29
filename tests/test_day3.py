import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Day3.Api_request import *
from Day3.Json_module import *
from Day3.file_handling import *

class TestDay3(unittest.TestCase):
    def test_dummy(self):
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
