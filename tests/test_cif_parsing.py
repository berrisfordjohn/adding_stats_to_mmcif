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

    def test_valid_cif(self):
        mh = mmcifHandling(fileName=self.test_files.TEST_VALID_MMCIF_FILE)
        s = mh.parse_mmcif()
        self.assertTrue(s)

    def test_exptl_valid_cif(self):
        self.test_files.one_sequence()
        mh = mmcifHandling(fileName=self.test_files.cif)
        s = mh.parse_mmcif()
        self.assertTrue(s)
        cat = 'exptl'
        ret_data = mh.getCategory(category=cat)
        self.assertTrue(ret_data == dict())
        exptl_data = mh.addExptlToCif()
        self.assertTrue(exptl_data == self.test_files.exptl_data)
        ret_data = mh.getCategory(category=cat)
        self.assertTrue(ret_data == self.test_files.exptl_data)


if __name__ == '__main__':
    unittest.main()
