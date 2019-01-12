#!/usr/bin/env python
from .cif_handling import mmcifHandling
import argparse
import logging

logger = logging.getLogger()
FORMAT = "%(filename)s - %(funcName)s - %(message)s"
logging.basicConfig(format=FORMAT)


def run_process(mmcif_to_add_data_to, input_cif):
    gc = GetCifData(input_cif)
    gc.run_process()
    data = gc.return_data()

    ac = AddToMmcif()
    ac.parse_mmcif(mmcif_file=mmcif_to_add_data_to)
    ac.add_to_cif(mmcif_file=mmcif_to_add_data_to, data_dictionary=data)


class GetCifData:

    def __init__(self, mmcif_file):
        self.mmcif_file = mmcif_file
        self.mmcif_data = dict()
        self.ch = mmcifHandling()

    def parse_cif(self):
        return self.ch.parse_mmcif(self.mmcif_file)

    def get_datablocks(self):
        return self.ch.getDatablocks()

    def get_datablock(self, datablock):
        if datablock in self.get_datablocks():
            return self.ch.getDatablock(datablock=datablock)
        return None

    def get_categories(self):
        return self.ch.getCategories()

    def run_process(self):
        if self.parse_cif():
            for datablock in self.get_datablocks():
                if self.get_datablock(datablock=datablock):
                    for category in self.get_categories():
                        self.mmcif_data.update(self.ch.getCategory(category=category))

    def return_data(self):
        return self.mmcif_data


class AddToMmcif:

    def _init__(self):
        self.ch = mmcifHandling()

    def parse_mmcif(self, mmcif_file):
        self.ch.parse_mmcif(mmcif_file)
        return self.ch.getDatablock(datablock=0)

    def add_to_cif(self, mmcif_file, data_dictionary):
        self.ch.addToCif(data_dictionary=data_dictionary)
        self.ch.writeCif(fileName=mmcif_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_mmcif', help='input mmcif file to get data from', type=str, required=True)
    parser.add_argument('--mmcif_to_add_data_to', help='mmcif file to add data to', type=str, required=True)
    parser.add_argument('-d', '--debug', help='debugging', action='store_const', dest='loglevel', const=logging.DEBUG,
                        default=logging.INFO)

    args = parser.parse_args()

    logger.setLevel(args.loglevel)

    run_process(mmcif_to_add_data_to=args.mmcif_to_add_data_to, input_cif=args.input_mmcif)
