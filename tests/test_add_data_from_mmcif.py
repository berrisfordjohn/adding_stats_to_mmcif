import unittest
import tempfile
import os
import shutil
from tests.access_test_files import TestFiles
from adding_stats_to_mmcif.add_data_from_mmcif import AddToMmcif


class TestAddDataFromMMCif(unittest.TestCase):

    def setUp(self):
        self.test_files = TestFiles()
        self.ac = AddToMmcif()
        self.simple = self.test_files.TEST_SIMPLE_CIF
        self.tempDir = tempfile.mkdtemp()
        self.outfile = os.path.join(self.tempDir, 'output.cif')

    def test_get_cif_data_run_process(self):
        ret = self.ac.get_data(mmcif_file=self.simple)
        self.assertTrue(ret == {'_category1.': {'item1': ['row1_v1', 'row2_v1'], 'item2': ['row1_v2', 'row2_v2']}})

    def test_add_to_mmcif_new_cat(self):
        data_dict = {'software': {'name': 'Aimless'}}
        ret = self.ac.add_to_cif(input_mmcif_file=self.simple, output_mmcif_file=self.outfile,
                                 data_dictionary=data_dict)
        self.assertTrue(ret)
        ret = self.ac.ch.getCategories()
        self.assertTrue(len(ret) == 2)

    def test_add_to_mmcif_existing_cat(self):
        category = 'category1'
        prepared_cat = self.ac.ch.prepareCategory(category=category)
        data_dict = {category: {'item1': 'row3_v1', 'item2': 'row3_v2'}}
        ret = self.ac.add_to_cif(input_mmcif_file=self.simple, output_mmcif_file=self.outfile,
                                 data_dictionary=data_dict)
        self.assertTrue(ret)
        ret = self.ac.ch.getCategories()
        self.assertTrue(len(ret) == 1)
        data = self.ac.ch.getCategory(category=category)
        self.assertTrue(data != dict())
        for item in data.get(prepared_cat, {}):
            values = data.get(prepared_cat, {}).get(item, [])
            self.assertTrue(len(values) == 3)

    def tearDown(self):
        if self.tempDir:
            shutil.rmtree(self.tempDir)


if __name__ == '__main__':
    unittest.main()
