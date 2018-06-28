#!/usr/bin/env python
from .cif_handling import mmcifHandling
import argparse
import logging

logger = logging.getLogger()
FORMAT = "%(filename)s - %(funcName)s - %(message)s"
logging.basicConfig(format=FORMAT)

class AddSequenceToMmcif:

    def __init__(self, input_mmcif, output_mmcif, fasta_file):
        self.input_mmcif = input_mmcif
        self.output_cif = output_mmcif
        self.fasta_file = fasta_file
        self.sequence_dict = dict()

    def process_fasta(self):
        pass

    



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--output_mmcif', help='output mmcif file', type=str, required=True)
    parser.add_argument('--input_mmcif', help='input mmcif file', type=str, required=True)
    parser.add_argument('--fasta_file', help='input fasta file', type=str, required=True)
    parser.add_argument('-d', '--debug', help='debugging', action='store_const', dest='loglevel', const=logging.DEBUG,
                        default=logging.INFO)

    args = parser.parse_args()

    logger.setLevel(args.loglevel)

    # input and output files
    fasta_file = args.fasta_file
    input_cif = args.input_mmcif
    output_cif = args.output_mmcif