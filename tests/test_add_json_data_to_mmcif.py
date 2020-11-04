import json
import os
import shutil
import tempfile
import unittest

from adding_stats_to_mmcif.add_json_data_to_mmcif import AddJsonDataToMmcif
from tests.access_test_files import TestFiles


class TestAddDataFromMMCif(unittest.TestCase):

    def setUp(self):
        self.test_files = TestFiles()
        self.ac = AddJsonDataToMmcif()
        self.simple_mmcif = self.test_files.TEST_SIMPLE_CIF
        self.simple_json = self.test_files.TEST_SIMPLE_JSON
        self.tempDir = tempfile.mkdtemp()
        self.outfile = os.path.join(self.tempDir, 'output.cif')

    def test_get_data(self):
        ret = self.ac.get_data(json_file=self.simple_json)
        self.assertTrue(ret == {"category1": {"item1": ["value1", "value2"],
                                              "item2": ["value1", "value2"]},
                                "category2": {"item3": "value"}
                                })

    def test_add_to_mmcif_new_cat(self):
        data = {"category2": {"item1": ["value1", "value2"],
                              "item2": ["value1", "value2"]},
                "category3": {"item3": "value"}
                }
        test_json = os.path.join(self.tempDir, 'test.json')
        with open(test_json, 'w') as out_file:
            json.dump(data, out_file)
        data_dict = self.ac.get_data(json_file=test_json)
        ret = self.ac.add_to_cif(input_mmcif_file=self.simple_mmcif, output_mmcif_file=self.outfile,
                                 data_dictionary=data_dict)
        self.assertTrue(ret)
        ret = self.ac.ch.getCategories()
        self.assertTrue(len(ret) == 3)

    def tearDown(self):
        if self.tempDir:
            shutil.rmtree(self.tempDir)


if __name__ == '__main__':
    unittest.main()
