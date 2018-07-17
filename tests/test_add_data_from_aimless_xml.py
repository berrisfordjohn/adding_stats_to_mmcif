import unittest
from tests.access_test_files import TestFiles
from adding_stats_to_mmcif.add_data_from_aimless_xml import get_xml_data, main


class TestAddDataFromAimless(unittest.TestCase):

    def setUp(self):
        self.test_files = TestFiles()

    def test_missing_file(self):
        xml_data, software_row = get_xml_data(xml_file='missing file')
        self.assertTrue(isinstance(xml_data, dict))
        self.assertTrue(software_row.get('version', None) is None)

    def test_good_aimless_file(self):
        xml_data, software_row = get_xml_data(xml_file=self.test_files.TEST_AIMLESS_XML_FILE)
        self.assertNotEqual(xml_data, dict())
        self.assertTrue(software_row.get('version', None) == "0.5.16")

    def test_non_aimless_file(self):
        xml_data, software_row = get_xml_data(xml_file=self.test_files.TEST_NON_AIMLESS_XML_FILE)
        self.assertEqual(xml_data, dict())
        self.assertTrue(software_row.get('version', None) is None)


if __name__ == '__main__':
    unittest.main()
