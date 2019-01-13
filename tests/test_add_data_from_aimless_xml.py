import unittest
import tempfile
import os
import shutil
from tests.access_test_files import TestFiles
from adding_stats_to_mmcif.add_data_from_aimless_xml import get_xml_data, run_process
from adding_stats_to_mmcif.cif_handling import mmcifHandling


class TestAddDataFromAimless(unittest.TestCase):

    def setUp(self):
        self.test_files = TestFiles()
        self.aimless_version = "0.5.16"

    def test_missing_file(self):
        xml_data, software_row = get_xml_data(xml_file='missing file')
        self.assertTrue(isinstance(xml_data, dict))
        self.assertTrue(software_row.get('version', None) is None)

    def test_good_aimless_file(self):
        xml_data, software_row = get_xml_data(xml_file=self.test_files.TEST_AIMLESS_XML_FILE)
        self.assertNotEqual(xml_data, dict())
        self.assertTrue(software_row.get('version', None) == self.aimless_version)

    def test_non_aimless_file(self):
        xml_data, software_row = get_xml_data(xml_file=self.test_files.TEST_NON_AIMLESS_XML_FILE)
        self.assertEqual(xml_data, dict())
        self.assertTrue(software_row.get('version', None) is None)

    def test_integration_writes_output_file(self):
        xml_file = self.test_files.TEST_AIMLESS_XML_FILE
        input_cif = self.test_files.TEST_VALID_MMCIF_FILE
        output_folder = tempfile.mkdtemp()
        output_cif = os.path.join(output_folder, 'output.cif')
        worked = run_process(xml_file=xml_file, input_cif=input_cif, output_cif=output_cif)
        self.assertTrue(worked)
        shutil.rmtree(output_folder)

    def test_integration_version_in_output_file(self):
        xml_file = self.test_files.TEST_AIMLESS_XML_FILE
        input_cif = self.test_files.TEST_VALID_MMCIF_FILE
        output_folder = tempfile.mkdtemp()
        output_cif = os.path.join(output_folder, 'output.cif')
        worked = run_process(xml_file=xml_file, input_cif=input_cif, output_cif=output_cif)
        self.assertTrue(worked)
        mm = mmcifHandling()
        worked = mm.parse_mmcif(fileName=output_cif)
        self.assertTrue(worked)
        software_cat = mm.getCategory(category='software')
        versions = software_cat['_software.']['version']
        names = software_cat['_software.']['name']
        print('FAILURE!!!')
        print(names)
        aimless_instance = None
        for instance, name in enumerate(names):
            if name == 'Aimless':
                aimless_instance = instance
        version = versions[aimless_instance]

        self.assertTrue(version == self.aimless_version)

        shutil.rmtree(output_folder)


if __name__ == '__main__':
    unittest.main()
