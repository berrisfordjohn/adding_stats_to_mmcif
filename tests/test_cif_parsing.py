import unittest

from tests.access_test_files import TestFiles
from adding_stats_to_mmcif.cif_handling import mmcifHandling


class TestXmlParsing(unittest.TestCase):

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

    def test_valid_cif(self):
        s = self.mh.parse_mmcif(fileName=self.test_files.TEST_VALID_MMCIF_FILE)
        self.assertTrue(s)

    def test_exptl_valid_cif(self):
        self.test_files.one_sequence()
        s = self.mh.parse_mmcif(fileName=self.test_files.cif)
        self.assertTrue(s)
        cat = 'exptl'
        ret_data = self.mh.getCategory(category=cat)
        self.assertTrue(ret_data == dict())
        exptl_data = self.mh.addExptlToCif()
        self.assertTrue(exptl_data == self.test_files.exptl_data)
        ret_data = self.mh.getCategory(category=cat)
        self.assertTrue(ret_data == self.test_files.exptl_data)


if __name__ == '__main__':
    unittest.main()
