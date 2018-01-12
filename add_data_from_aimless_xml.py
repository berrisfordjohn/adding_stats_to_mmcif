#!/usr/bin/env python
from aimless_xml_parser import aimlessReport
from cif_handling import mmcifHandling
import argparse
import logging

logger = logging.getLogger()

def aimless_software_row():
    software_row = {}
    software_row['name'] = 'Aimless'
    software_row['classification'] = 'data scaling'

    return software_row

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--output_mmcif', help='output mmcif file', type=str, required=True)
    parser.add_argument('--input_mmcif', help='input mmcif file', type=str, required=True)
    parser.add_argument('--xml_file', help='input xml file', type=str, required=True)
    parser.add_argument('-d', '--debug', help='debugging', action='store_const', dest='loglevel', const=logging.DEBUG,
                        default=logging.INFO)

    args = parser.parse_args()

    logger.setLevel(args.loglevel)

    xml_file = args.xml_file
    input_cif = args.input_mmcif
    output_cif = args.output_mmcif

    ar = aimlessReport(xml_file=xml_file)
    xml_data = ar.return_data()
    if xml_data:
        pc = mmcifHandling(fileName=input_cif)
        pc.parse_mmcif()
        pc.addToCif(data_dictionary=xml_data)
        aimless_dict = aimless_software_row()
        software_cat = pc.addValuesToCategory(category='software', item_value_dictionary=aimless_dict, ordinal_item='pdbx_ordinal')
        pc.addToCif(data_dictionary=software_cat)
        pc.writeCif(fileName=output_cif)
