import unittest
import os
from tests.access_test_files import TestFiles

from adding_stats_to_mmcif.aimless_xml_parser import aimlessReport

class TestAimlessReportGeneration(unittest.TestCase):

    def setUp(self):

        self.test_files = TestFiles()

    def test_xml_none_type(self):
        s = aimlessReport(xml_file=None).parse_xml()
        self.assertFalse(s)

    def test_xml_does_not_exists(self):
        s = aimlessReport(xml_file='does_not_exist.xml').parse_xml()
        self.assertFalse(s)

    def test_bad_xml_file(self):
        s = aimlessReport(xml_file=self.test_files.TEST_BAD_XML_FILE).parse_xml()
        self.assertFalse(s)

    def test_non_aimless_xml_file(self):
        s = aimlessReport(xml_file=self.test_files.TEST_NON_AIMLESS_XML_FILE).parse_xml()
        self.assertFalse(s)
    
    def test_aimless_xml_file(self):
        s = aimlessReport(xml_file=self.test_files.TEST_AIMLESS_XML_FILE).parse_xml()
        self.assertTrue(s)

    def test_aimless_version_good_xml_file(self):
        s = aimlessReport(xml_file=self.test_files.TEST_AIMLESS_XML_FILE)
        version = s.get_aimlesss_version()
        self.assertEqual(version, "0.5.16")

    def test_aimless_version_non_aimless_xml_file(self):
        s = aimlessReport(xml_file=self.test_files.TEST_NON_AIMLESS_XML_FILE)
        version = s.get_aimlesss_version()
        self.assertIsNone(version)

    def test_aimless_data_non_aimless_xml_file(self):
        s = aimlessReport(xml_file=self.test_files.TEST_NON_AIMLESS_XML_FILE)
        data = s.return_data()
        self.assertTrue(isinstance(data, dict))
        self.assertEqual(data, dict())

    def test_aimless_data_aimless_xml_file(self):
        s = aimlessReport(xml_file=self.test_files.TEST_AIMLESS_XML_FILE)
        data = s.return_data()
        self.assertTrue(isinstance(data, dict))
        self.assertNotEqual(data, dict())
    
    def test_aimless_data_aimless_xml_file_no_data(self):
        s = aimlessReport(xml_file=self.test_files.TEST_AIMLESS_XML_FILE_NO_DATA)
        data = s.return_data()
        self.assertTrue(isinstance(data, dict))
        self.assertEqual(data, dict())
    

if __name__ == '__main__':
    unittest.main()