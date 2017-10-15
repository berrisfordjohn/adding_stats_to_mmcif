#!/usr/bin/env python
import aimless_xml_parser
import pdbe_cif_handling
import pprint
import logging
import argparse
logger = logging.getLogger()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_cif', help='output mmcif file', type=str, required=True)
    parser.add_argument('--input_mmcif', help='input mmcif file', type=str, required=True)
    parser.add_argument('--xml_file', help='input xml file', type=str, required=True)
    parser.add_argument('-d', '--debug', help='debugging', action='store_const', dest='loglevel', const=logging.DEBUG,
                        default=logging.INFO)

    args = parser.parse_args()

    logger.setLevel(args.loglevel)

    xml_file = args.xml_file
    input_cif = args.input_cif
    output_cif = args.output_cif
    ar = aimless_xml_parser.aimlessReport(xml_file=xml_file)
    xml_data = ar.return_data()
    if xml_data:
        pc = pdbe_cif_handling.mmcifHandling(fileName=input_cif)
        pc.parse_mmcif()
        pc.addToCif(data_dictionary=xml_data)
        pc.writeCif(fileName=output_cif)
