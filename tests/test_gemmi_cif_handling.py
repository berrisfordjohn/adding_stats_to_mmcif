import unittest
import logging
from tests.access_test_files import TestFiles
from adding_stats_to_mmcif.gemmi_cif_handling import mmcifHandling

logger = logging.getLogger()
FORMAT = "%(filename)s - %(funcName)s - %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)

class TestGemmiCifHandling(unittest.TestCase):

    def setUp(self):
        self.test_files = TestFiles()
        self.mh = mmcifHandling()

    def test_none_type(self):
        s = self.mh.parse_mmcif(fileName=None)
        self.assertFalse(s)

    def test_none_existing_file(self):
        s = self.mh.parse_mmcif(fileName='missing_file.cif')
        self.assertFalse(s)

    def test_invalid_cif(self):
        s = self.mh.parse_mmcif(fileName=self.test_files.TEST_INVALID_MMCIF_FILE)
        self.assertFalse(s)

    def test_valid_cif(self):
        s = self.mh.parse_mmcif(fileName=self.test_files.TEST_VALID_MMCIF_FILE)
        self.assertTrue(s)

    def test_simple_cif(self):
        s = self.mh.parse_mmcif(fileName=self.test_files.TEST_SIMPLE_CIF)
        self.assertTrue(s)

    def test_get_datablocks_by_num(self):
        s = self.mh.parse_mmcif(fileName=self.test_files.TEST_SIMPLE_CIF)
        self.assertTrue(s)
        for position, datablock in enumerate(self.mh.getDatablocks()):
            ret = self.mh.getDatablock(datablock=position)
            self.assertTrue(ret)

    def test_get_datablocks_by_name(self):
        s = self.mh.parse_mmcif(fileName=self.test_files.TEST_SIMPLE_CIF)
        self.assertTrue(s)
        for datablock in self.mh.getDataBlockNames():
            ret = self.mh.getDatablock(datablock=datablock)
            self.assertTrue(ret)

    def test_prepare_category(self):
        category = 'test'
        result = '_test.'
        ret = self.mh.prepare_cat(category=category)
        self.assertTrue(ret == result)
        ret = self.mh.prepare_cat(category=result)
        self.assertTrue(ret == result)

    def test_getCategory(self):
        self.mh.parse_mmcif(fileName=self.test_files.TEST_SIMPLE_CIF)
        self.mh.getDatablock(0)
        category = '_category1.'
        self.assertTrue(category in self.mh.getCategories())
        self.assertTrue(len(self.mh.getCategories()) == 1)

    def test_setCategory_new_category(self):
        self.mh.parse_mmcif(fileName=self.test_files.TEST_SIMPLE_CIF)
        self.mh.getDatablock(0)
        category = 'category2'
        item_value_dict = {'item1': ['value1']}
        self.mh.setCategory(category=category, item_value_dict=item_value_dict)
        ret = self.mh.getCategory(category=category)
        self.assertTrue(ret == {'_category2.': item_value_dict})

    def test_setCategory_existing_category(self):
        self.mh.parse_mmcif(fileName=self.test_files.TEST_SIMPLE_CIF)
        self.mh.getDatablock(0)
        category = 'category1'
        prepared_cat = self.mh.prepare_cat(category=category)
        self.assertTrue(prepared_cat in self.mh.getCategories())
        item_value_dict = {'item1': ['row1_v1', 'row2_v1', 'row3_v1'], 'item2': ['row1_v2', 'row2_v2', 'row3_v2']}
        result = {prepared_cat: item_value_dict}
        self.mh.setCategory(category=category, item_value_dict=item_value_dict)
        ret = self.mh.getCategory(category=category)
        self.assertTrue(ret == result)

    def test_getCatItemValues(self):
        self.mh.parse_mmcif(fileName=self.test_files.TEST_SIMPLE_CIF)
        self.mh.getDatablock(0)
        category = 'category1'
        item = 'item1'
        values = ['row1_v1', 'row2_v1']
        ret = self.mh.getCatItemValues(category=category, item=item)
        self.assertTrue(ret == values)
        category = '_category1.'
        ret = self.mh.getCatItemValues(category=category, item=item)
        self.assertTrue(ret == values)

    def test_getCatItemsValues(self):
        self.mh.parse_mmcif(fileName=self.test_files.TEST_SIMPLE_CIF)
        self.mh.getDatablock(0)
        category = 'category1'
        item = 'item1'
        values = ['row1_v1', 'row2_v1']
        result = {item: values}
        ret = self.mh.getCatItemsValues(category=category, items=[item])
        self.assertTrue(ret == result)


if __name__ == '__main__':
    unittest.main()
