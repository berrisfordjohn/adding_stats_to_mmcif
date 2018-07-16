#!/usr/bin/env python
import logging # pragma: no cover
import mmCif.mmcifIO as mmcif # pragma: no cover
import pprint # pragma: no cover
import os # pragma: no cover
import argparse # pragma: no cover

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
        '''parse the mmcif and return a dictionary file'''
        cfr = mmcif.CifFileReader()
        try:
            if os.path.exists(self.f):
                # parse the cif file
                if not self.atom_site:
                    self.cifObj = cfr.read(self.f, output='cif_file', ignore=["_atom_site", "_atom_site_anisotrop"])
                else:
                    self.cifObj = cfr.read(self.f, output='cif_file')

                if self.cifObj:
                    return True
            return False

        except Exception as e:
            logging.error("unable to parse mmcif file: %s" % self.f)
            logging.error(e)

        return False

    def getDatablock(self):
        datablocks = self.cifObj.getDataBlockIds()
        logging.debug('datablocks:')
        logging.debug(datablocks)
        self.cif_categories = self.cifObj.getDataBlocks()[self.datablock]

    def getDataBlockWithMostCat(self):
        logging.debug('getDataBlockWithMostCat')
        largest_num = 0
        datablockToGet = None
        datablocks = self.cifObj.getDataBlockIds()
        logging.debug(datablocks)
        for datablock in datablocks:
            logging.debug(datablock)
            cif_categories = self.cifObj.getDataBlock(datablock)
            cats = cif_categories.getCategoryIds()
            logging.debug(cats)
            num_cats = len(cats)
            if num_cats > largest_num:
                largest_num = num_cats
                datablockToGet = datablock
        logging.debug('datablock with most cat: %s' % datablockToGet)
        self.cif_categories = self.cifObj.getDataBlock(datablockToGet)

    def getDataBlockWithAtomSite(self):
        logging.debug('getDataBlockWithAtomSite')
        datablockToGet = None
        datablocks = self.cifObj.getDataBlockIds()
        logging.debug(datablocks)
        for datablock in datablocks:
            logging.debug(datablock)
            cif_categories = self.cifObj.getDataBlock(datablock)
            cats = cif_categories.getCategoryIds()
            logging.debug(cats)
            if 'atom_site' in cats:
                datablockToGet = datablock
        logging.debug('datablock with most cat: %s' % datablockToGet)
        self.cif_categories = self.cifObj.getDataBlock(datablockToGet)

    def prepare_cat(self, category):
        self.category = category
        if not self.cif_categories:
            self.getDatablock()
        if self.category[0] != '_':
            self.category = '_' + self.category
        return self.category

    def getCategoryObject(self, category):
        category = self.prepare_cat(category=category)
        category_1 = self.cif_categories.getCategory(category)
        return category_1

    def getCatItemValues(self, category, item):
        category = self.prepare_cat(category=category)
        values = self.cif_categories.getCategory(category=category).getItem(item_name=item).value

        return values

    def getCategory(self, category):
        mmcif_dictionary = dict()
        self.prepare_cat(category=category)
        logging.debug('getCategory')
        logging.debug(self.category)
        full_category = self.getCategoryObject(category=category)
        logging.debug(full_category)
        if full_category:
            items = self.cif_categories.getCategory(category=self.category).getItemNames()
            for cif_item in items:
                values = self.getCatItemValues(category=self.category, item=cif_item)
                mmcif_dictionary.setdefault(category, {})[cif_item] = values

        return mmcif_dictionary

    def addValuesToCategory(self, category, item_value_dictionary, ordinal_item=None):
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
            current_values = {}
            for mmcif_item in item_value_dictionary:
                current_values.setdefault(category)[mmcif_item] = [item_value_dictionary[mmcif_item]]
                if mmcif_item == ordinal_item:
                    current_values.setdefault(category)[mmcif_item] = ['1']

        return current_values

    def removeCategory(self, category):
        category = self.prepare_cat(category=category)
        self.cif_categories.setCategory(category=category).remove()

    def addToCif(self, data_dictionary):
        try:
            if data_dictionary:
                for category in data_dictionary:
                    self.prepare_cat(category=category)
                    self.removeCategory(category=category)
                    for item in data_dictionary[category]:
                        values = data_dictionary[category][item]
                        logging.debug('setting: %s.%s to %s' % (self.category, item, ','.join(values)))
                        self.cif_categories.setCategory(self.category).setItem(item).setValue(values)
        except Exception as e:
            logging.error(e)

    def writeCif(self, fileName):
        cfd1 = mmcif.CifFileWriter(fileName)
        cfd1.write(self.cifObj, preserve_order=True)


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
    mh = mmcifHandling(fileName=input_cif)
    parsed_cif = mh.parse_mmcif()
    if parsed_cif:
        #mh.getDataBlockWithMostCat()
        mh.getDataBlockWithAtomSite()
        test_dict = mh.getCategory(category=cat)
        mh.removeCategory(category=cat)
        mh.removeCategory(category='fake_cat')
        fake_data = {'test_cat': {'item1': ['1', '2', '3'], 'item2': ['2', '3', '4']}}
        mh.addToCif(data_dictionary=fake_data)
        mh.writeCif(fileName=output_cif)
