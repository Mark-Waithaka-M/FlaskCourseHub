import unittest
from test import myTest

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(myTest)
    unittest.TextTestRunner(verbosity=2).run(suite)