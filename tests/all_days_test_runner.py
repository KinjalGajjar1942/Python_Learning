import unittest
import os

if __name__ == "__main__":
    test_dir = os.path.dirname(__file__)
    suite = unittest.defaultTestLoader.discover(test_dir, pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
