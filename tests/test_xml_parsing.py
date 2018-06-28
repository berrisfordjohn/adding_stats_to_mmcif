import unittest

from tests.access_test_files import TestFiles

from adding_stats_to_mmcif.xml_parsing import parse_xml

class TestXmlParsing(unittest.TestCase):

    def setUp(self):

        self.test_files = TestFiles()

    def test_none_type(self):
        s = parse_xml(xml_file=None)
        self.assertIsNone(s)
    
    def test_none_existing_file(self):
        s = parse_xml(xml_file='does_not_exist')
        self.assertIsNone(s)

    def test_existing_file_but_not_xml(self):
        s = parse_xml(xml_file='does_not_exist')
        self.assertIsNone(s)

    def test_existing_file_is_xml(self):
        s = parse_xml(xml_file=self.test_files.TEST_AIMLESS_XML_FILE)
        self.assertIsNotNone(s)

    def test_invalid_xml_file(self):
        s = parse_xml(xml_file=self.test_files.TEST_BAD_XML_FILE)
        self.assertIsNone(s)


if __name__ == '__main__':
    unittest.main()