#!/usr/bin/env python
import logging
import argparse

from pdbe_cif_handling import mmcifHandling as pdbe_cif_handling
from gemmi_cif_handling import mmcifHandling as gemmi_cif_handling

logger = logging.getLogger()


class mmcifHandling:
    def __init__(self, fileName, datablock=0, atom_site=True):
        #self.cif_handling = pdbe_cif_handling(fileName=fileName, datablock=datablock, atom_site=atom_site)
        self.cif_handling = gemmi_cif_handling(fileName=fileName, datablock=datablock, atom_site=atom_site)

    def parse_mmcif(self):
        '''parse the mmcif and return a dictionary file'''
        parsed_cif = self.cif_handling.parse_mmcif()
        if parsed_cif:
            return True
        return False

    def getDatablock(self):
        self.cif_categories = self.cif_handling.getDatablock()

    def getCategoryObject(self, category):
        category_1 = self.cif_handling.getCategory(category)
        return category_1

    def getCatItemValues(self, category, item):
        values = self.cif_handling.getCatItemValues(category=category, item=item)
        return values

    def getCategory(self, category):
        mmcif_dictionary = self.cif_handling.getCategory(category=category)
        return mmcif_dictionary

    def removeCategory(self, category):
        self.cif_handling.removeCategory(category=category)

    def addToCif(self, data_dictionary):
        self.cif_handling.addToCif(data_dictionary=data_dictionary)

    def writeCif(self, fileName):
        self.cif_handling.writeCif(fileName=fileName)


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
