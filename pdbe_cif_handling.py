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
        items = self.cif_categories.getCategory(category=self.category).getItemNames()
        for cif_item in items:
            values = self.getCatItemValues(category=self.category, item=cif_item)
            mmcif_dictionary.setdefault(category, {})[cif_item] = values

        return mmcif_dictionary

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
    logger.setLevel(logging.DEBUG)
    cat = 'reflns'
    cif_file = 'test_data/3zt9.cif'
    mh = mmcifHandling(fileName=cif_file)
    mh.parse_mmcif()
    test_dict = mh.getCategory(category=cat)
    pprint.pprint(test_dict)
    mh.removeCategory(category=cat)
    mh.removeCategory(category='fake_cat')
    fake_data = {'test_cat': {'item1': [1, 2, 3], 'item2': [2, 3, 4]}}
    mh.addToCif(mmcif_dictionary=fake_data)
    mh.writeCif(fileName=cif_file + 'test')
