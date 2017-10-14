#!/usr/bin/env python
import logging
import mmCif.mmcifIO as mmcif
import pprint

logger = logging.getLogger()


class mmcifHandling:
    def __init__(self, fileName, datablock=0, atom_site=False):
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
            # parse the cif file
            if not self.atom_site:
                self.cifObj = cfr.read(self.f, output='cif_file', ignore=["_atom_site", "_atom_site_anisotrop"])
            else:
                self.cifObj = cfr.read(self.f, output='cif_file')

        except Exception as e:
            logging.error("unable to parse mmcif file: %s" % self.f)
            logging.error(e)

        return self.cifObj

    def getDatablock(self):
        datablocks = self.cifObj.getDataBlockIds()
        logging.debug('datablocks:')
        logging.debug(datablocks)
        self.cif_categories = self.cifObj.getDataBlocks()[self.datablock]

    def prepare_cat(self, category):
        self.category = category
        if not self.cif_categories:
            self.getDatablock()
        if self.category[0] != '_':
            self.category = '_' + self.category

    def getCategory(self, category):
        self.prepare_cat(category=category)
        category_1 = self.cif_categories.getCategory(self.category)
        return category_1

    def getCatItemValues(self, category, item):
        self.prepare_cat(category=category)
        values = self.cif_categories.getCategory(category=self.category).getItem(item_name=item).value

        return values

    def getCatDict(self, category):
        mmcif_dictionary = dict()
        self.prepare_cat(category=category)
        items = self.cif_categories.getCategory(category=self.category).getItemNames()
        for cif_item in items:
            values = self.getCatItemValues(category=category, item=cif_item)
            mmcif_dictionary.setdefault(category, {})[cif_item] = values

        return mmcif_dictionary

    def getCatList(self, category):
        if not self.cif_categories:
            self.getDatablock()
        if category[0] != '_':
            category = '_' + category
        if category in self.cif_categories:
            logging.debug('Category %s found' % category)
            for item in self.cif_categories[category]:
                value = self.cif_categories[category][item]
                if not isinstance(value, list):
                    self.cif_categories[category][item] = [value]
            return self.cif_categories[category]
        else:
            logging.debug('Category %s not found' % category)
            return None

    def addToCif(self, mmcif_dictionary):
        for cat in mmcif_dictionary:
            for item in mmcif_dictionary[cat]:
                self.cif_categories.setCategory(cat).setItem(item).setValue(mmcif_dictionary[cat][item])

    def writeCif(self, fileName):
        cfd1 = mmcif.CifFileWriter(fileName)
        cfd1.write(self.cifObj, preserve_order=True)

    def reformat_dict_to_list(self, catDict):
        output_format = dict()
        for cif_cat in catDict:
            number_of_instances = len(catDict[cif_cat])
            for instance, values in enumerate(catDict[cif_cat]):
                for cif_item in values:
                    value = values[cif_item]
                    output_format.setdefault(cif_cat, {}).setdefault(cif_item, [''] * number_of_instances)[
                        instance] = value

        return output_format


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    cat = 'reflns'
    cif_file = 'test_data/3zt9.cif'
    mh = mmcifHandling(fileName=cif_file)
    mh.parse_mmcif()
    test_dict = mh.getCatDict(category=cat)
    pprint.pprint(test_dict)
    fake_data = {'test_cat': {'item1': [1, 2, 3], 'item2': [2, 3, 4]}}
    mh.addToCif(mmcif_dictionary=fake_data)
    mh.writeCif(fileName=cif_file + 'test')
