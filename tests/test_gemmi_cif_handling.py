import unittest
from tests.access_test_files import TestFiles

from adding_stats_to_mmcif.gemmi_cif_handling import mmcifHandling


class TestGemmiCifHandling(unittest.TestCase):

    def setUp(self):
        self.test_files = TestFiles()
        self.mh = mmcifHandling()

    def test_none_type(self):
        s = self.mh.parse_mmcif(fileName=None)
        self.assertFalse(s)

    def test_none_existing_file(self):
        s = self.mh.parse_mmcif(fileName='missing_file.cif')
        self.assertFalse(s)

    def test_invalid_cif(self):
        s = self.mh.parse_mmcif(fileName=self.test_files.TEST_INVALID_MMCIF_FILE)
        self.assertFalse(s)

    def test_valid_cif(self):
        s = self.mh.parse_mmcif(fileName=self.test_files.TEST_VALID_MMCIF_FILE)
        self.assertTrue(s)
