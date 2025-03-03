import unittest
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
from unittests.test_des import TestDes

class TestRunner:
    def __init__(self):
        pass

    def run_all_tests(self):  # Added 'self'
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()

        # Add tests from each test case
        for test_class in [TestDes]:
            tests = loader.loadTestsFromTestCase(test_class)
            suite.addTests(tests)

        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        return result
        
if __name__ == "__main__":
    # Run unit tests
    test_result = TestRunner().run_all_tests()
    
    if not test_result.wasSuccessful():
        sys.exit("Unit tests failed. Aborting execution.")