import unittest
import tempfile
import os
import shutil
from tests.access_test_files import TestFiles
from adding_stats_to_mmcif.mmcif_dictionary_handling import SoftwareClassification


class TestSoftwareRow(unittest.TestCase):

    def setUp(self):
        self.mdh = SoftwareClassification()
        pass

    def test_software_dictionary(self):
        software_name = 'Aimless'
        software_version = "0.5.16"
        software_classification = 'data scaling'
        result = {'name': software_name, 'classification': software_classification,
                  'version': software_version}
        software_row = self.mdh.get_software_row(software_name=software_name, version=software_version)
        self.assertTrue(result == software_row)

    def test_software_dictionary_no_version(self):
        software_name = 'Aimless'
        software_classification = 'data scaling'
        result = {'name': software_name, 'classification': software_classification}
        software_row = self.mdh.get_software_row(software_name=software_name)
        self.assertTrue(result == software_row)

    def test_software_dictionary_incorrect_case(self):
        software_name = 'AIMLESS'
        software_classification = 'data scaling'
        result = {'name': 'Aimless', 'classification': software_classification}
        software_row = self.mdh.get_software_row(software_name=software_name)
        print(software_row)
        self.assertTrue(result == software_row)

    def test_software_dictionary_unknown_software(self):
        software_name = 'UNKNOWN'
        software_classification = ''
        result = {'name': software_name, 'classification': software_classification}
        software_row = self.mdh.get_software_row(software_name=software_name)
        self.assertTrue(result == software_row)

    def test_software_dictionary_two_classification(self):
        software_name = 'ADDREF'
        software_classification = 'data scaling'
        result = {'name': software_name, 'classification': software_classification}
        software_row = self.mdh.get_software_row(software_name=software_name)
        self.assertTrue(result == software_row)



if __name__ == '__main__':
    unittest.main()
