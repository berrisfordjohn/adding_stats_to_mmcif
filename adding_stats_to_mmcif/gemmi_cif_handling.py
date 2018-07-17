#!/usr/bin/env python
import logging
from gemmi import cif
import pprint
import os
import argparse

logger = logging.getLogger()


class mmcifHandling:
    def __init__(self, fileName, datablock=0, atom_site=True):
        self.f = fileName
        self.cifObj = None
        self.atom_site = atom_site
        self.datablock = datablock
        self.cif_categories = None
        self.category = None

    def parse_mmcif(self):
        """parse the mmcif and return a dictionary file"""
        # from http://gemmi.readthedocs.io/en/latest/cif-parser.html#python-module
        if self.f and os.path.exists(self.f):
            try:
                self.cifObj = cif.read_file(self.f)  # copy all the data from mmCIF file
                if self.cifObj:
                    # self.getDataBlockWithMostCat()
                    self.getDataBlockWithAtomSite()
                    # self.getDatablock()
                    return True
            except Exception as e:
                logging.error(e)
        return False

    def getDatablock(self):
        if not self.cifObj:
            self.parse_mmcif()
        logging.debug('datablocks')
        logging.debug(self.cifObj)
        try:
            if self.datablock in self.cifObj:
                self.cif_categories = self.cifObj[self.datablock]
                return True
        except Exception as e:
            logging.error(e)
        return False

    def getDataBlockWithMostCat(self):
        if not self.cifObj:
            self.parse_mmcif()
        logging.debug('getDataBlockWithMostCat')
        largest_num = 0
        datablockToGet = None
        for position, datablock in enumerate(self.cifObj):
            logging.debug(datablock)
            cif_categories = self.cifObj[position]
            cats = cif_categories.get_mmcif_category_names()
            logging.debug(cats)
            num_cats = len(cats)
            if num_cats > largest_num:
                largest_num = num_cats
                datablockToGet = position
        logging.debug('datablock with most cat: %s' % datablockToGet)
        self.cif_categories = self.cifObj[datablockToGet]

    def getDataBlockWithAtomSite(self):
        if not self.cifObj:
            self.parse_mmcif()
        logging.debug('getDataBlockWithAtomSite')
        datablockToGet = None
        for position, datablock in enumerate(self.cifObj):
            logging.debug(datablock)
            cif_categories = self.cifObj[position]
            atom_site = cif_categories.find_values('_atom_site.id')
            # logging.debug(atom_site)
            if atom_site:
                datablockToGet = position
        logging.debug('datablock with atom_site cat: %s' % datablockToGet)
        self.cif_categories = self.cifObj[datablockToGet]

    def prepare_cat(self, category):
        self.category = category
        if not self.cif_categories:
            self.getDatablock()
        if self.category[0] != '_':
            self.category = '_' + self.category
        if self.category[-1] != '.':
            self.category = self.category + '.'
        return self.category

    def getCatItemsValues(self, category, items):
        if not self.cifObj:
            self.parse_mmcif()
        result_dict = dict()
        category = self.prepare_cat(category=category)
        table_view = self.cif_categories.find(category, items)
        for row in table_view:
            for position, k in enumerate(items):
                result_dict.setdefault(k, []).append(row.str(position))
        return result_dict

    def getCatItemValues(self, category, item):
        if not self.cifObj:
            self.parse_mmcif()
        items = [item]
        result_dict = self.getCatItemsValues(category=category, items=items)
        values = result_dict[item]
        return values

    def getCategory(self, category):
        if not self.cifObj:
            self.parse_mmcif()
        logging.debug('getCategory')
        mmcif_dictionary = dict()
        category = self.prepare_cat(category=category)

        cat = self.cif_categories.find_mmcif_category(category)
        if cat:
            for cif_item in cat.tags:
                cif_item = cif_item.split('.')[-1]
                logging.debug('mmCIF item: %s' % cif_item)
                values = self.getCatItemValues(category=category, item=cif_item)
                mmcif_dictionary.setdefault(category, {})[cif_item] = values

        return mmcif_dictionary

    def getCategoryList(self, category):
        if not self.cifObj:
            self.parse_mmcif()
        self.prepare_cat(category=category)
        mmcif_dictionary = self.getCategory(category=self.category)
        # logging.debug(mmcif_dictionary)

        mmcif_cat_list = list()
        if self.category in mmcif_dictionary:
            first_key_in_mmcif_dict = list(mmcif_dictionary[self.category].keys())[0]
            len_of_values = len(mmcif_dictionary[self.category][first_key_in_mmcif_dict])
            mmcif_cat_list = [{} for i in range(1, len_of_values + 1)]
            for item in mmcif_dictionary[self.category]:
                for position, value in enumerate(mmcif_dictionary[self.category][item]):
                    mmcif_cat_list[position][item] = value

        return mmcif_cat_list

    def addValuesToCategory(self, category, item_value_dictionary, ordinal_item=None):
        if not self.cifObj:
            self.parse_mmcif()
        category = self.prepare_cat(category=category)
        current_values = self.getCategory(category=category)
        if current_values:
            if category in current_values:
                for mmcif_item in current_values[category]:
                    num_current_items = len(current_values[category][mmcif_item])
                    if mmcif_item in item_value_dictionary:
                        current_values[category][mmcif_item].append(item_value_dictionary[mmcif_item])
                    elif mmcif_item == ordinal_item:
                        ordinal = num_current_items + 1
                        current_values[category][mmcif_item].append(str(ordinal))
                    else:
                        current_values[category][mmcif_item].append('')
        else:
            for mmcif_item in item_value_dictionary:
                current_values.setdefault(category, {})[mmcif_item] = [item_value_dictionary[mmcif_item]]
                if mmcif_item == ordinal_item:
                    current_values.setdefault(category, {})[mmcif_item] = ['1']

        return current_values

    def removeCategory(self, category):
        category = self.prepare_cat(category=category)
        # self.cif_categories.delete_category(category)
        pass

    def addToCif(self, data_dictionary):
        if not self.cifObj:
            self.parse_mmcif()
        logging.debug('addToCif')
        logging.debug(data_dictionary)
        try:
            if data_dictionary:
                for category in data_dictionary:
                    values = data_dictionary[category]
                    category = self.prepare_cat(category=category)
                    # self.removeCategory(category=category)
                    self.cif_categories.set_mmcif_category(category, values)
            return True
        except Exception as e:
            logging.error(e)
        return False

    def writeCif(self, fileName):
        if not self.cifObj:
            return False
        logging.debug('writing out to {}'.format(fileName))
        self.cifObj.write_file(fileName)
        if os.path.exists(fileName):
            return True
        return False


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--output_mmcif', help='output mmcif file', type=str, required=True)
    parser.add_argument('--input_mmcif', help='input mmcif file', type=str, required=True)
    parser.add_argument('-d', '--debug', help='debugging', action='store_const', dest='loglevel', const=logging.DEBUG,
                        default=logging.INFO)

    args = parser.parse_args()

    logger.setLevel(args.loglevel)

    input_cif = args.input_mmcif
    output_cif = args.output_mmcif

    cat = 'struct_conf'
    items = ['id', 'beg_label_comp_id']
    mh = mmcifHandling(fileName=input_cif)
    parsed_cif = mh.parse_mmcif()
    if parsed_cif:
        logging.debug('cif parsed')
        logging.debug(mh.cif_categories)
        test = mh.getCatItemsValues(category=cat, items=items)
        print(test)
        fake_data = {'test_cat': {'item1': ['1', '2', '3'], 'item2': ['2', '3', '4']}}
        added = mh.addToCif(data_dictionary=fake_data)
        mh.writeCif(fileName=output_cif)
    else:
        logging.error('unable to parse mmcif')
