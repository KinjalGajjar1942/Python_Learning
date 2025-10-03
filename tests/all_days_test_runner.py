import unittest
import sys
import os

def run_all_tests():
    """Run all test files in the tests directory"""
    # Add the parent directory to the path for imports
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    # Discover and run all test files
    test_dir = os.path.dirname(__file__)
    suite = unittest.defaultTestLoader.discover(test_dir, pattern="test_*.py")
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(
        verbosity=2,
        stream=sys.stdout,
        descriptions=True,
        failfast=False
    )
    
    print("="*70)
    print("RUNNING ALL PYTHON LEARNING PROJECT TESTS")
    print("="*70)
    
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print(f"\nFAILED TESTS:")
        for test, traceback in result.failures:
            print(f"- {test}")
    
    if result.errors:
        print(f"\nERROR TESTS:")
        for test, traceback in result.errors:
            print(f"- {test}")
    
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0
    print(f"\nSuccess Rate: {success_rate:.1f}%")
    print("="*70)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
