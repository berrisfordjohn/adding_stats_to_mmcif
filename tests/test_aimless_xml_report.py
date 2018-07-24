import unittest
from tests.access_test_files import TestFiles

from adding_stats_to_mmcif.aimless_xml_parser import aimlessReport, split_on_separator


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

    def test_split_separator(self):
        value_to_split = 'the quick brown fox'
        data = split_on_separator(separator=' ', value_to_split=value_to_split)
        self.assertTrue(data == value_to_split.split(' '))
        value_to_split_comma = 'the,quick,brown,fox'
        data = split_on_separator(separator=',', value_to_split=value_to_split_comma)
        self.assertTrue(data == value_to_split_comma.split(','))
        data = split_on_separator(separator=None, value_to_split=value_to_split)
        self.assertTrue(data == list())
        value_to_split_T = 'theTquickTbrownTfox'
        data = split_on_separator(separator='T', value_to_split=value_to_split_T)
        self.assertTrue(data == value_to_split_T.split('T'))


if __name__ == '__main__':
    unittest.main()
