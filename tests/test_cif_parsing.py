import unittest

from tests.access_test_files import TestFiles
from adding_stats_to_mmcif.cif_handling import mmcifHandling


class TestXmlParsing(unittest.TestCase):

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

    def test_exptl_valid_cif(self):
        self.test_files.one_sequence()
        s = self.mh.parse_mmcif(fileName=self.test_files.cif)
        self.assertTrue(s)
        cat = 'exptl'
        ret_data = self.mh.getCategory(category=cat)
        self.assertTrue(ret_data == dict())
        exptl_data = self.mh.addExptlToCif()
        self.assertTrue(exptl_data == self.test_files.exptl_data)
        ret_data = self.mh.getCategory(category=cat)

        self.assertTrue(ret_data == self.test_files.exptl_data)

    def test_addValuesToCategory_no_existing_cat(self):
        category = 'test'
        prepared_category = self.mh.prepareCategory(category=category)
        item_value_dictionary = {'item1': 'value1'}
        result = {prepared_category: {'item1': ['value1']}}
        ret = self.mh.addValuesToCategory(category=category, item_value_dictionary=item_value_dictionary)
        self.assertTrue(ret == result)
        item_value_dictionary = {'item1': ['value1']}
        ret = self.mh.addValuesToCategory(category=category, item_value_dictionary=item_value_dictionary)
        self.assertTrue(ret == {prepared_category: item_value_dictionary})
        item_value_dictionary = {'item1': ['value1', 'value2'],
                                 'item2': ['value3', 'value4'],
                                 'item3': ['value5', 'value6']}
        ret = self.mh.addValuesToCategory(category=category, item_value_dictionary=item_value_dictionary)
        self.assertTrue(ret == {prepared_category: item_value_dictionary})

    def test__addValuesToCategory_existing_cat(self):
        ok = self.mh.parse_mmcif(self.test_files.TEST_SIMPLE_CIF)
        self.assertTrue(ok)
        ok = self.mh.getDatablock(0)
        self.assertTrue(ok)
        existing_cat = 'category1'
        prepared_existing_cat = self.mh.prepareCategory(category=existing_cat)
        category = 'test'
        prepared_cat = self.mh.prepareCategory(category=category)
        item_value_dictionary = {'item1': 'value1'}
        ret = self.mh.addValuesToCategory(category=category, item_value_dictionary=item_value_dictionary)
        self.assertTrue(ret == {prepared_cat: {'item1': ['value1']}})
        item_value_dictionary = {'item1': 'row3_v1', 'item2': 'row3_v2'}
        result = {prepared_existing_cat: {'item1': ['row1_v1', 'row2_v1', 'row3_v1'],
                                          'item2': ['row1_v2', 'row2_v2', 'row3_v2']}}
        ret = self.mh.addValuesToCategory(category=existing_cat, item_value_dictionary=item_value_dictionary)
        self.assertTrue(ret == result)
        item_value_dictionary = {'item1': ['row3_v1'], 'item2': ['row3_v2']}
        ret = self.mh.addValuesToCategory(category=existing_cat, item_value_dictionary=item_value_dictionary)
        self.assertTrue(ret == result)

    def test_addToCif_new_category(self):
        ok = self.mh.parse_mmcif(self.test_files.TEST_SIMPLE_CIF)
        self.assertTrue(ok)
        ok = self.mh.getDatablock(0)
        self.assertTrue(ok)
        data_dictionary = {'category2': {'item1': 'value1'}}
        ok = self.mh.addToCif(data_dictionary=data_dictionary)
        self.assertTrue(ok)
        self.assertTrue(len(self.mh.getCategories()) == 2)

    def test_addToCif_existing_category(self):
        ok = self.mh.parse_mmcif(self.test_files.TEST_SIMPLE_CIF)
        self.assertTrue(ok)
        ok = self.mh.getDatablock(0)
        self.assertTrue(ok)
        category = 'category1'
        prepared_cat = self.mh.prepareCategory(category=category)
        data_dictionary = {category: {'item1': 'row3_v1', 'item2': 'row3_v2'}}
        result = {prepared_cat: {'item1': ['row1_v1', 'row2_v1', 'row3_v1'],
                                 'item2': ['row1_v2', 'row2_v2', 'row3_v2']}}
        ok = self.mh.addToCif(data_dictionary=data_dictionary)
        self.assertTrue(ok)

        ret = self.mh.getCategory(category)
        self.assertTrue(ret == result)

    def test_check_string_list(self):
        value = 'test'
        ret = self.mh.check_string_list(value=value)
        self.assertTrue(ret == ['test'])

        value = ['test']
        ret = self.mh.check_string_list(value=value)
        self.assertTrue(ret == ['test'])

        value = ['v1', 'v2']
        ret = self.mh.check_string_list(value=value)
        self.assertTrue(ret == ['v1', 'v2'])

    def test_addValuesToCategory_not_all_items(self):
        category = 'software'
        prepared_cat = self.mh.prepareCategory(category=category)
        to_add = {'name': 'Aimless', 'classification': 'data scaling', 'version': 'test'}
        self.mh.parse_mmcif(fileName=self.test_files.TEST_VALID_MMCIF_FILE)
        ret = self.mh.getCategory(category=category)
        expected_num = len(ret.get(prepared_cat, {}).get('name', [])) + 1
        ret = self.mh.addValuesToCategory(category=category, item_value_dictionary=to_add, ordinal_item='pdbx_ordinal')
        for item in ret.get(prepared_cat, {}):
            actual_len = len(ret.get(prepared_cat, {}).get(item, []))
            self.assertTrue(expected_num == actual_len)


if __name__ == '__main__':
    unittest.main()
