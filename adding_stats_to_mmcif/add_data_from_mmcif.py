#!/usr/bin/env python
import argparse
import logging
from pprint import pprint

from adding_stats_to_mmcif.cif_handling import mmcifHandling

logger = logging.getLogger()
FORMAT = "%(filename)s - %(funcName)s - %(message)s"
logging.basicConfig(format=FORMAT)


class AddToMmcif:

    def __init__(self):
        self.mmcif_data = dict()
        self.ch = mmcifHandling()

    def get_data(self, mmcif_file):
        if self.ch.parse_mmcif(fileName=mmcif_file):
            for position, datablock in enumerate(self.ch.getDatablocks()):
                if self.ch.getDatablock(datablock=position):
                    for category in self.ch.getCategories():
                        self.mmcif_data.update(self.ch.getCategory(category=category))

        return self.mmcif_data

    def add_to_cif(self, input_mmcif_file, output_mmcif_file, data_dictionary):
        try:
            self.ch.parse_mmcif(fileName=input_mmcif_file)
            ret = self.ch.addToCif(data_dictionary=data_dictionary)
            if ret:
                self.ch.writeCif(fileName=output_mmcif_file)
                return True
            return False
        except Exception as e:
            logging.error(e)
            return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_data_mmcif', help='input mmcif file to get data from', type=str, required=True)
    parser.add_argument('--input_model_mmcif', help='mmcif file to add data to', type=str, required=True)
    parser.add_argument('--output_model_mmcif', help='mmcif file to add data to', type=str, required=True)
    parser.add_argument('-d', '--debug', help='debugging', action='store_const', dest='loglevel', const=logging.DEBUG,
                        default=logging.INFO)

    args = parser.parse_args()

    logger.setLevel(args.loglevel)

    ret = False
    gc = AddToMmcif()
    data = gc.get_data(args.input_data_mmcif)
    if data:
        pprint(data)
        ret = gc.add_to_cif(input_mmcif_file=args.input_model_mmcif, output_mmcif_file=args.output_model_mmcif,
                            data_dictionary=data)
    logging.info('worked: {}'.format(ret))
