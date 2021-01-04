#!/usr/bin/env python
import argparse
import logging

from .gemmi_cif_handling import mmcifHandling as gemmi_cif_handling

logger = logging.getLogger()


class mmcifHandling:
    def __init__(self):
        self.cif_handling = gemmi_cif_handling()

    def parse_mmcif(self, fileName):
        """
        parse the mmcif
        return True if worked, False if failed
        """
        if self.cif_handling.parse_mmcif(fileName=fileName):
            if len(self.getDatablocks()) > 0:
                if self.getDatablock():
                    return True
        return False

    def getDatablocks(self):
        return self.cif_handling.getDataBlockNames()

    def getDatablock(self, datablock=0):
        return self.cif_handling.getDatablock(datablock=datablock)

    def prepareCategory(self, category):
        return self.cif_handling.prepare_cat(category=category)

    def getCategories(self):
        return self.cif_handling.getCategories()

    def getCategoryObject(self, category):
        return self.cif_handling.getCategory(category)

    def getCatItemValues(self, category, item):
        return self.cif_handling.getCatItemValues(category=category, item=item)

    def getCategory(self, category):
        return self.cif_handling.getCategory(category=category)

    def getCategoryList(self, category):
        return self.cif_handling.getCategoryAsList(category=category)

    def setCategory(self, category, item_value_dict):
        self.cif_handling.setCategory(category=category, item_value_dict=item_value_dict)

    def removeCategory(self, category):
        self.setCategory(category=category, item_value_dict={})

    def writeCif(self, fileName):
        self.cif_handling.writeCif(fileName=fileName)

    def addToCif(self, data_dictionary):
        logging.debug(data_dictionary)
        if self.cif_handling.datablock:
            try:
                if data_dictionary:
                    for category in data_dictionary:
                        logging.debug(category)
                        item_value_dict = data_dictionary[category]
                        logging.debug('item value dict {}'.format(item_value_dict))
                        cat_item_value_dict = self.addValuesToCategory(category=category,
                                                                       item_value_dictionary=item_value_dict)
                        logging.debug('cat item dict {}'.format(cat_item_value_dict))
                        category = self.prepareCategory(category=category)
                        if cat_item_value_dict:
                            self.setCategory(category, cat_item_value_dict[category])
                        else:
                            return False
                return True
            except Exception as e:
                logging.error(e)
        else:
            logging.error('no datablock set')
        return False

    def mergeCategory(self, category, item_value_dictionary):
        category = self.prepareCategory(category=category)
        current_values = self.getCategory(category=category)
        for mmcif_item in item_value_dictionary:
            values = self.check_string_list(item_value_dictionary[mmcif_item])
            current_values[category][mmcif_item] = values
        return current_values

    def addValuesToCategory(self, category, item_value_dictionary, ordinal_item=None):
        logging.debug('addValuesToCategory')
        category = self.prepareCategory(category=category)
        current_values = self.getCategory(category=category)
        num_new_values = 0
        num_current_values = 0
        for key in item_value_dictionary:
            num_new_values = len(self.check_string_list(item_value_dictionary[key]))
        if current_values:
            if category in current_values:
                logging.debug(current_values)
                current_mmcif_items = current_values[category].keys()
                new_mmcif_items = item_value_dictionary.keys()
                for mmcif_item in current_values[category]:
                    num_current_values = len(current_values[category][mmcif_item])
                if set(current_mmcif_items) & set(new_mmcif_items):
                    logging.debug('overlap between input and output category')
                    for mmcif_item in current_values[category]:
                        num_current_items = len(current_values[category][mmcif_item])
                        if mmcif_item in item_value_dictionary:
                            new_values = self.check_string_list(item_value_dictionary[mmcif_item])
                            current_values[category][mmcif_item].extend(new_values)
                        elif mmcif_item == ordinal_item:
                            for pos in range(num_new_values):
                                ordinal = num_current_items + pos + 1
                                current_values[category][mmcif_item].append(str(ordinal))
                        else:
                            empty_values = [''] * num_new_values
                            current_values[category][mmcif_item].extend(empty_values)
                            # elif num_current_items == 0:
                else:
                    logging.debug('no overlap between new and current items')
                    if num_new_values == num_current_values:
                        logging.debug('same number of values')
                        current_values = self.mergeCategory(category=category,
                                                            item_value_dictionary=item_value_dictionary)
                    else:
                        logging.error('different number of values')
                        return {}
        else:
            for mmcif_item in item_value_dictionary:
                new_values = self.check_string_list(item_value_dictionary[mmcif_item])
                current_values.setdefault(category, {}).setdefault(mmcif_item, []).extend(new_values)

        return current_values

    @staticmethod
    def check_string_list(value):
        if type(value) == list:
            return value
        else:
            return [str(value)]

    def addExptlToCif(self, method='X-RAY DIFFRACTION'):
        entry_id = ''
        entry_ids = self.getCatItemValues(category='entry', item='id')
        if entry_ids:
            for entry in entry_ids:
                entry_id = entry
        cat = 'exptl'
        exptl_cat = self.getCategory(category=cat)
        if not exptl_cat:
            row = {'entry_id': entry_id, 'method': method}
            exptl_cat = self.addValuesToCategory(category=cat, item_value_dictionary=row)
            self.addToCif(data_dictionary=exptl_cat)
        return exptl_cat


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

    cat = 'reflns'
    mh = mmcifHandling()
    parsed_cif = mh.parse_mmcif(fileName=input_cif)
    if parsed_cif:
        logging.debug('parsed mmcif')
        test_dict = mh.getCategory(category=cat)
        logging.debug(test_dict)
        mh.removeCategory(category=cat)
        logging.debug('removed: %s' % cat)
        fake_data = {'test_cat': {'item1': ['1', '2', '3'], 'item2': ['2', '3', '4']}}
        mh.addToCif(data_dictionary=fake_data)
        logging.debug('added fake data')
        mh.writeCif(fileName=output_cif)
        logging.debug('written out: %s' % output_cif)
    else:
        logging.error('failed to parse mmcif')
