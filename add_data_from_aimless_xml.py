#!/usr/bin/env python
import aimless_xml_parser
import pdbe_cif_handling
import pprint
import logging

logger = logging.getLogger()


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    xml_file = 'test_data/gam-pipe.xml'
    cif_file = 'test_data/3zt9.cif'
    ar = aimless_xml_parser.aimlessReport(xml_file=xml_file)
    xml_data = ar.return_data()
    if xml_data:
        pc = pdbe_cif_handling.mmcifHandling(fileName=cif_file)
        pc.parse_mmcif()
        pc.addToCif(data_dictionary=xml_data)
        pc.writeCif(fileName=cif_file + 'output')