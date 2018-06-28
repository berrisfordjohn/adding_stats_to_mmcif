#!/usr/bin/env python
from .aimless_xml_parser import aimlessReport
from .cif_handling import mmcifHandling
import argparse
import logging

logger = logging.getLogger()
FORMAT = "%(filename)s - %(funcName)s - %(message)s"
logging.basicConfig(format=FORMAT)


def aimless_software_row(version=''):
    software_row = {}
    software_row['name'] = 'Aimless'
    software_row['classification'] = 'data scaling'
    if version:
        software_row['version'] = version

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

    # input and output files
    xml_file = args.xml_file
    input_cif = args.input_mmcif
    output_cif = args.output_mmcif

    # get data from aimless XML file
    ar = aimlessReport(xml_file=xml_file)
    xml_data = ar.return_data()
    aimless_version = ar.get_aimlesss_version()
    if xml_data:
        # if there is data from the XNL file then add this to the mmCIF file
        pc = mmcifHandling(fileName=input_cif)
        pc.parse_mmcif()
        # add aimless data to the mmCIF file
        pc.addToCif(data_dictionary=xml_data)
        #update the software list in the mmCIF file to add aimless
        aimless_dict = aimless_software_row(version=aimless_version)
        software_cat = pc.addValuesToCategory(category='software', item_value_dictionary=aimless_dict, ordinal_item='pdbx_ordinal')
        pc.addToCif(data_dictionary=software_cat)
        # write out the resulting mmCIF file.
        pc.writeCif(fileName=output_cif)
