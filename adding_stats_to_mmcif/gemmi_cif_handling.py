#!/usr/bin/env python
import logging
from gemmi import cif
import pprint
import os
import argparse

logger = logging.getLogger()


class mmcifHandling:
    def __init__(self):
        self.cifObj = None
        self.datablock = None
        self.category = None

    def parse_mmcif(self, fileName):
        """parse the mmcif and return a dictionary file"""
        # from http://gemmi.readthedocs.io/en/latest/cif-parser.html#python-module
        if fileName and os.path.exists(fileName):
            try:
                self.cifObj = cif.read_file(fileName)  # copy all the data from mmCIF file
                if self.cifObj:
                    return True
            except Exception as e:
                logging.error(e)
        return False

    def getDatablocks(self):
        return self.cifObj

    def getDataBlockNames(self):
        blocks = list()
        for position, block in enumerate(self.cifObj):
            blocks.append(block.name)
        return blocks

    def getDatablock(self, datablock=0):
        if self.cifObj:
            if type(datablock) == int:
                if len(self.getDatablocks()) >= datablock:
                    self.datablock = self.cifObj[datablock]
                    return True
            elif type(datablock) == str:
                if datablock in self.getDataBlockNames():
                    self.datablock = self.cifObj[datablock]
                    return True
        return False

    def getDataBlockWithMostCat(self):
        if self.cifObj:
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
            self.datablock = self.cifObj[datablockToGet]
        return self.datablock

    def getDataBlockWithAtomSite(self):
        if self.cifObj:
            logging.debug('getDataBlockWithAtomSite')
            datablockToGet = None
            for position, datablock in enumerate(self.cifObj):
                logging.debug(datablock)
                self.datablock = self.cifObj[position]
                atom_site = self.datablock.find_values('_atom_site.id')
                # logging.debug(atom_site)
                if atom_site:
                    datablockToGet = position
            logging.debug('datablock with atom_site cat: %s' % datablockToGet)
            self.datablock = self.cifObj[datablockToGet]
            return self.datablock
        return False

    def prepare_cat(self, category):
        self.category = category
        if self.category[0] != '_':
            self.category = '_' + self.category
        if self.category[-1] != '.':
            self.category = self.category + '.'
        return self.category

    def getCategories(self):
        if self.datablock:
            return self.datablock.get_mmcif_category_names()
        return None

    def getCatItemsValues(self, category, items):
        result_dict = dict()
        if self.datablock:
            category = self.prepare_cat(category=category)
            table_view = self.datablock.find(category, items)
            for row in table_view:
                for position, k in enumerate(items):
                    result_dict.setdefault(k, []).append(row.str(position))
        return result_dict

    def getCatItemValues(self, category, item):
        items = [item]
        result_dict = self.getCatItemsValues(category=category, items=items)
        values = result_dict[item]
        return values

    def getCategory(self, category):
        logging.debug('getCategory')
        mmcif_dictionary = dict()
        if self.datablock:
            category = self.prepare_cat(category=category)
            cat = self.datablock.find_mmcif_category(category)
            if cat:
                for cif_item in cat.tags:
                    cif_item = cif_item.split('.')[-1]
                    logging.debug('mmCIF item: %s' % cif_item)
                    values = self.getCatItemValues(category=category, item=cif_item)
                    mmcif_dictionary.setdefault(category, {})[cif_item] = values

        return mmcif_dictionary

    def getCategoryAsList(self, category):
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
        category = self.prepare_cat(category=category)
        current_values = self.getCategory(category=category)
        if current_values:
            if category in current_values:
                for mmcif_item in current_values[category]:
                    new_value = item_value_dictionary[mmcif_item]
                    if type(new_value) == str:
                        new_value = [new_value]
                    num_new_values = len(new_value)
                    num_current_items = len(current_values[category][mmcif_item])
                    if mmcif_item in item_value_dictionary:
                        current_values[category][mmcif_item].extend(new_value)
                    elif mmcif_item == ordinal_item:
                        for pos in range(num_new_values):
                            ordinal = num_current_items + pos + 1
                            current_values[category][mmcif_item].append(str(ordinal))
                    else:
                        empty_values = [''] * num_new_values
                        current_values[category][mmcif_item].extend(empty_values)
        else:
            for mmcif_item in item_value_dictionary:
                new_value = item_value_dictionary[mmcif_item]
                if type(new_value) == str:
                    new_value = [new_value]
                num_new_values = len(new_value)
                if mmcif_item == ordinal_item:
                    for pos in range(num_new_values):
                        ordinal = pos + 1
                        current_values.setdefault(category, {}).setdefault(mmcif_item, []).append(str(ordinal))
                else:
                    current_values.setdefault(category, {}).setdefault(mmcif_item, []).extend(new_value)

        return current_values

    def removeCategory(self, category):
        category = self.prepare_cat(category=category)
        # self.cif_categories.delete_category(category)
        pass

    def addToCif(self, data_dictionary):
        logging.debug('addToCif')
        logging.debug(data_dictionary)
        if self.datablock:
            try:
                if data_dictionary:
                    for category in data_dictionary:
                        category = self.prepare_cat(category=category)
                        item_value_dict = data_dictionary[category]
                        item_value_dict = self.addValuesToCategory(category=category, item_value_dictionary=item_value_dict)
                        self.datablock.set_mmcif_category(category, item_value_dict)
                return True
            except Exception as e:
                logging.error(e)
        else:
            logging.error('no datablock set')
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
        mh.getDatablock()
        logging.debug(mh.datablock)
        test = mh.getCatItemsValues(category=cat, items=items)
        print(test)
        fake_data = {'test_cat': {'item1': ['1', '2', '3'], 'item2': ['2', '3', '4']}}
        added = mh.addToCif(data_dictionary=fake_data)
        mh.writeCif(fileName=output_cif)
    else:
        logging.error('unable to parse mmcif')
