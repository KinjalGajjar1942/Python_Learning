
import unittest
import importlib.util
import sys
import os

day2_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Day2'))
sys.path.insert(0, day2_path)

modules = [
    'Dictionaries',
    'List_Comprehensions',
    'Lists',
    'Sets',
    'Tuple',
    'loop',
]
for mod in modules:
    spec = importlib.util.spec_from_file_location(mod, os.path.join(day2_path, f"{mod}.py"))
    module = importlib.util.module_from_spec(spec)
    sys.modules[mod] = module
    spec.loader.exec_module(module)

class TestDay2(unittest.TestCase):
    def test_dummy(self):
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
