#!/usr/bin/env python
from adding_stats_to_mmcif.cif_handling import mmcifHandling
import argparse
import logging

logger = logging.getLogger()
FORMAT = "%(filename)s - %(funcName)s - %(message)s"
logging.basicConfig(format=FORMAT)


class AddToMmcif:

    def __init__(self):
        self.mmcif_data = dict()
        self.ch = mmcifHandling()

    def get_data(self, mmcif_file):
        if self.ch.parse_mmcif(fileName=mmcif_file):
            for datablock in self.ch.getDatablocks():
                if self.ch.getDatablock(datablock=datablock):
                    for category in self.ch.getCategories():
                        self.mmcif_data.update(self.ch.getCategory(category=category))

        return self.mmcif_data

    def add_to_cif(self, input_mmcif_file, output_mmcif_file, data_dictionary):
        try:
            self.ch.parse_mmcif(fileName=input_mmcif_file)
            self.ch.addToCif(data_dictionary=data_dictionary)
            self.ch.writeCif(fileName=output_mmcif_file)
            return True
        except Exception as e:
            logging.error(e)
            return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_mmcif', help='input mmcif file to get data from', type=str, required=True)
    parser.add_argument('--mmcif_to_add_data_to', help='mmcif file to add data to', type=str, required=True)
    parser.add_argument('-d', '--debug', help='debugging', action='store_const', dest='loglevel', const=logging.DEBUG,
                        default=logging.INFO)

    args = parser.parse_args()

    logger.setLevel(args.loglevel)

    ret = False
    gc = AddToMmcif()
    data = gc.get_data(args.input_mmcif)
    if data:
        ret = gc.add_to_cif(input_mmcif_file=args.mmcif_to_add_data_to, output_mmcif_file=args.mmcif_to_add_data_to,
                            data_dictionary=data)
    logging.info('worked: {}'.format(ret))
