#!/usr/bin/env python
import logging
import argparse

from .gemmi_cif_handling import mmcifHandling as gemmi_cif_handling

logger = logging.getLogger()


class mmcifHandling:
    def __init__(self, fileName, datablock=0, atom_site=True):
        # self.cif_handling = pdbe_cif_handling(fileName=fileName, datablock=datablock, atom_site=atom_site)
        self.cif_handling = gemmi_cif_handling(fileName=fileName, datablock=datablock, atom_site=atom_site)

    def parse_mmcif(self):
        """
        parse the mmcif
        return True if worked, False if failed
        """
        return self.cif_handling.parse_mmcif()

    def getDatablock(self):
        return self.cif_handling.getDatablock()

    def getCategoryObject(self, category):
        return self.cif_handling.getCategory(category)

    def getCatItemValues(self, category, item):
        return self.cif_handling.getCatItemValues(category=category, item=item)

    def getCategory(self, category):
        return self.cif_handling.getCategory(category=category)

    def getCategoryList(self, category):
        return self.cif_handling.getCategoryList(category=category)

    def addValuesToCategory(self, category, item_value_dictionary, ordinal_item=None):
        return self.cif_handling.addValuesToCategory(category=category, item_value_dictionary=item_value_dictionary,
                                                     ordinal_item=ordinal_item)

    def removeCategory(self, category):
        self.cif_handling.removeCategory(category=category)

    def addToCif(self, data_dictionary):
        self.cif_handling.addToCif(data_dictionary=data_dictionary)

    def writeCif(self, fileName):
        self.cif_handling.writeCif(fileName=fileName)

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
