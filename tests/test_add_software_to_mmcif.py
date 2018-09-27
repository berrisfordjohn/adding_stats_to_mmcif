import unittest
import tempfile
import os
import shutil
import logging
from tests.access_test_files import TestFiles
from adding_stats_to_mmcif.mmcif_dictionary_handling import SoftwareClassification
from adding_stats_to_mmcif.add_software_to_mmcif import AddSoftwareToMmcif

logger = logging.getLogger()
FORMAT = "%(filename)s - %(funcName)s - %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)


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


class TestAddSoftware(unittest.TestCase):

    def setUp(self):
        self.test_files = TestFiles()
        pass

    def test_get_software_row(self):
        software_name = 'AIMLESS'
        software_classification = 'data scaling'
        result = {'name': 'Aimless', 'classification': software_classification}
        addsoft = AddSoftwareToMmcif(input_cif=None, output_cif=None, software_list=None)
        software_row = addsoft.get_software_row(software=software_name)
        self.assertTrue(software_row == result)

    def test_single_software_row(self):
        software_name = 'AIMLESS'
        software_classification = 'data scaling'
        result = {'name': 'Aimless', 'classification': software_classification}
        addsoft = AddSoftwareToMmcif(input_cif=None, output_cif=None, software_list=[{'pgm': software_name}])
        software_row = addsoft.process_input_software_dict(software_dict=addsoft.input_software_list[0])
        self.assertTrue(software_row == result)

    def test_parse_good_file(self):
        self.test_files.one_sequence()
        addsoft = AddSoftwareToMmcif(input_cif=self.test_files.cif, output_cif=None, software_list=[])
        parsed = addsoft.parse_mmcif()
        self.assertTrue(parsed)

    def test_parse_missing_file(self):
        self.test_files.one_sequence()
        addsoft = AddSoftwareToMmcif(input_cif='missing.cif', output_cif=None, software_list=[])
        parsed = addsoft.parse_mmcif()
        self.assertFalse(parsed)

    def test_existing_software(self):
        self.test_files.one_sequence()
        software_result = ['refmac']
        addsoft = AddSoftwareToMmcif(input_cif=self.test_files.cif, output_cif=None, software_list=[])
        addsoft.parse_mmcif()
        existing_software = addsoft.get_existing_software()
        self.assertTrue(existing_software == software_result)

    def test_add_single_software_row(self):
        self.test_files.one_sequence()
        temp_dir = tempfile.mkdtemp()
        output_cif = os.path.join(temp_dir, 'output.cif')
        software_name = 'aimless'
        software_classification = 'data scaling'
        software_version = '2.0'
        addsoft = AddSoftwareToMmcif(input_cif=self.test_files.cif,
                                     output_cif=output_cif,
                                     software_list=[{'pgm': software_name, 'version': software_version}])
        addsoft.run_process()
        self.assertTrue(os.path.exists(output_cif))

        addsoft_result = AddSoftwareToMmcif(input_cif=output_cif, output_cif=None, software_list=[])
        software_list = addsoft_result.get_existing_software()
        self.assertTrue(software_list.sort() == ['refmac', 'Aimless'].sort())

        shutil.rmtree(temp_dir)

    def test_two_single_software_row(self):
        self.test_files.one_sequence()
        temp_dir = tempfile.mkdtemp()
        output_cif = os.path.join(temp_dir, 'output.cif')
        input_software = [{'pgm': 'aimless'}, {'pgm': 'xia2'}]
        addsoft = AddSoftwareToMmcif(input_cif=self.test_files.cif,
                                     output_cif=output_cif,
                                     software_list=input_software)
        addsoft.run_process()
        self.assertTrue(os.path.exists(output_cif))

        addsoft_result = AddSoftwareToMmcif(input_cif=output_cif, output_cif=None, software_list=[])
        software_list = addsoft_result.get_existing_software()
        self.assertTrue(software_list.sort() == ['refmac', 'Aimless', 'XIA2'].sort())

        shutil.rmtree(temp_dir)


if __name__ == '__main__':
    unittest.main()
