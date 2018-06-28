import unittest

from tests.access_test_files import TestFiles
from adding_stats_to_mmcif.cif_handling import mmcifHandling

class TestXmlParsing(unittest.TestCase):

    def setUp(self):

        self.test_files = TestFiles()

    def test_none_type(self):
        mh = mmcifHandling(fileName=None)
        s = mh.parse_mmcif()
        self.assertFalse(s)
    
    def test_none_existing_file(self):
        mh = mmcifHandling(fileName='missing_file.cif')
        s = mh.parse_mmcif()
        self.assertFalse(s)

    def test_invalid_cif(self):
        mh = mmcifHandling(fileName=self.test_files.TEST_INVALID_MMCIF_FILE)
        s = mh.parse_mmcif()
        self.assertFalse(s)

    def test_valid_cif(self):
        mh = mmcifHandling(fileName=self.test_files.TEST_VALID_MMCIF_FILE)
        s = mh.parse_mmcif()
        self.assertTrue(s)