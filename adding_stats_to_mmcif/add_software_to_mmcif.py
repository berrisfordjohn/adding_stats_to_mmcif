#!/usr/bin/env python
import os
import sys
import json
from .cif_handling import mmcifHandling
from .mmcif_dictionary_handling import SoftwareClassification
import argparse
import logging

logger = logging.getLogger()
FORMAT = "%(filename)s - %(funcName)s - %(message)s"
logging.basicConfig(format=FORMAT)


class AddSoftwareToMmcif:

    def __init__(self, input_cif, output_cif, software_list=None, software_file=None):
        self.input_cif = input_cif
        self.output_cif = output_cif
        self.input_software_list = software_list
        self.input_software_file = software_file
        self.existing_software = list()
        self.software_row = dict()
        self.mm = mmcifHandling(fileName=self.input_cif)
        self.sc = SoftwareClassification()

    def parse_mmcif(self):
        parsed = self.mm.parse_mmcif()
        if not parsed:
            logging.error('unable to parse mmcif: {}'.format(self.input_cif))
        return parsed

    def process_software_file(self):
        try:
            if os.path.exists(self.input_software_file):
                with open(self.input_software_file) as infile:
                    self.input_software_list = json.load(infile)
            else:
                logging.error('{} not found'.format(self.input_software_file))
        except Exception as e:
            logging.error(e)

    def get_existing_software(self):
        self.existing_software = self.mm.getCatItemValues(category='software', item='name')

        return self.existing_software

    def add_software_row(self):
        software_cat = self.mm.addValuesToCategory(category='software', item_value_dictionary=self.software_row,
                                                   ordinal_item='pdbx_ordinal')
        self.mm.addToCif(data_dictionary=software_cat)

    def get_software_row(self, software, classification=None, version=None):
        self.software_row = self.sc.get_software_row(software_name=software,
                                                     classification=classification,
                                                     version=version)
        return self.software_row

    def is_software_in_existing_software(self, software):
        software = self.sc.get_software_name_correct_case(software_name=software)
        if self.existing_software:
            if software in self.existing_software:
                return True
        return False

    @staticmethod
    def check_input_software_dict(software_dict):
        logging.info(software_dict)
        if software_dict and isinstance(software_dict, dict):
            return True
        logging.error('unable to read software list row')
        return False

    def check_input_software_list(self):
        if self.input_software_list and isinstance(self.input_software_list, list):
            return True
        logging.error('unable to read software list')
        return False

    def process_input_software_dict(self, software_dict):
        if self.check_input_software_dict(software_dict=software_dict):
            software_name = software_dict.get('pgm', '')
            software_version = software_dict.get('version', '')
            software_classification = software_dict.get('classification', '')

            if software_name:
                software_name = self.sc.get_software_name_correct_case(software_name=software_name)
                if not self.is_software_in_existing_software(software=software_name):
                    self.get_software_row(software=software_name, classification=software_classification,
                                          version=software_version)
        return self.software_row

    def run_process(self):
        if self.input_software_file:
            self.process_software_file()
        parsed = self.parse_mmcif()
        if parsed:
            if self.check_input_software_list():
                for row in self.input_software_list:
                    self.process_input_software_dict(software_dict=row)
                    if self.software_row:
                        software_cat = self.mm.addValuesToCategory(category='software',
                                                                   item_value_dictionary=self.software_row,
                                                                   ordinal_item='pdbx_ordinal')
                        self.mm.addToCif(data_dictionary=software_cat)

                self.mm.writeCif(fileName=self.output_cif)
                if os.path.exists(self.output_cif):
                    return True
        return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_mmcif', help='output mmcif file', type=str, required=True)
    parser.add_argument('--input_mmcif', help='input mmcif file', type=str, required=True)
    parser.add_argument('--software_file', help='input file containing software list', required=True, type=str)
    parser.add_argument('-d', '--debug', help='debugging', action='store_const', dest='loglevel', const=logging.DEBUG,
                        default=logging.INFO)

    args = parser.parse_args()

    logger.setLevel(args.loglevel)
    add_soft = AddSoftwareToMmcif(software_file=args.software_file, input_cif=args.input_mmcif,
                                  output_cif=args.output_mmcif)
    worked = add_soft.run_process()
    if not worked:
        logging.error('Adding software failed')
        sys.exit(1)
