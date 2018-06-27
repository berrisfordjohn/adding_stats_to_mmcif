import unittest

from adding_stats_to_mmcif.tests import (test_xml_parsing, test_aimless_xml_report, test_cif_parsing)

@unittest.skip("This is not a unittest")
class TestSuite(unittest.TestCase):
    
    def __init__(self, verbosity=0):
        self.verbosity = verbosity
        self._suite = self._create_test_suite()

    def _create_test_suite(self):
        loader = unittest.TestLoader()

        Test_Suite = unittest.TestSuite()
        Test_Suite = loader.loadTestsFromModule(test_xml_parsing)
        Test_Suite.addTests(loader.loadTestsFromModule(test_aimless_xml_report))
        Test_Suite.addTests(loader.loadTestsFromModule(test_cif_parsing))
        
        return Test_Suite 

    def _run(self):
        result = unittest.TextTestRunner(verbosity=self.verbosity).run(self._suite)

    def run_all_tests(self):
        self._run()

if __name__ == '__main__':
    suite = TestSuite(verbosity=2)
    suite.run_all_tests()