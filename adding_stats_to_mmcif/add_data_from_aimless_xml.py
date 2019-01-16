#!/usr/bin/env python
from .aimless_xml_parser import aimlessReport
from .cif_handling import mmcifHandling
import argparse
import logging
import os

logger = logging.getLogger()
FORMAT = "%(filename)s - %(funcName)s - %(message)s"
logging.basicConfig(format=FORMAT)


def get_xml_data(xml_file):
    # get data from aimless XML file
    ar = aimlessReport(xml_file=xml_file)
    xml_data = ar.return_data()
    software_row = ar.get_aimless_version_dict()

    return xml_data, software_row


def run_process(xml_file, input_cif, output_cif):
    xml_data, software_row = get_xml_data(xml_file=xml_file)
    if xml_data:
        # if there is data from the XML file then add this to the mmCIF file
        if os.path.exists(input_cif):
            pc = mmcifHandling()
            pc.parse_mmcif(fileName=input_cif)
            # add aimless data to the mmCIF file
            ok = pc.addToCif(data_dictionary=xml_data)
            # update the software list in the mmCIF file to add aimless
            software_cat = pc.addValuesToCategory(category='software', item_value_dictionary=software_row,
                                                  ordinal_item='pdbx_ordinal')
            ok = pc.addToCif(data_dictionary=software_cat)
            # add exptl data
            pc.addExptlToCif()
            # write out the resulting mmCIF file.
            pc.writeCif(fileName=output_cif)
            if os.path.exists(output_cif):
                return True
    return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_mmcif', help='output mmcif file', type=str, required=True)
    parser.add_argument('--input_mmcif', help='input mmcif file', type=str, required=True)
    parser.add_argument('--xml_file', help='input xml file', type=str, required=True)
    parser.add_argument('-d', '--debug', help='debugging', action='store_const', dest='loglevel', const=logging.DEBUG,
                        default=logging.INFO)

    args = parser.parse_args()

    logger.setLevel(args.loglevel)

    run_process(xml_file=args.xml_file, input_cif=args.input_mmcif, output_cif=args.output_mmcif)
