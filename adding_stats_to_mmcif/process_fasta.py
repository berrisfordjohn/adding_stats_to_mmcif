#!/usr/bin/env python
from Bio import SeqIO 
import logging 
import argparse 
import os 

logger = logging.getLogger()
FORMAT = "%(filename)s - %(funcName)s - %(message)s"
logging.basicConfig(format=FORMAT)

class processFasta:

    def __init__(self, fasta_file):
        self.fasta_file = fasta_file
        self.sequence_dict = dict()

    def process_fasta_file(self):
        if self.fasta_file:
            logging.debug('fasta file: {}'.format(self.fasta_file))
            if os.path.exists(self.fasta_file):
                logging.debug('processing fasta file')
                self.fasta_data = SeqIO.parse(self.fasta_file, "fasta")
                for record in self.fasta_data:
                    self.sequence_dict[record.id] = record.seq

    def get_sequence_dict(self):
        return self.sequence_dict

if __name__ == '__main__': 
    parser = argparse.ArgumentParser()
    parser.add_argument('--fasta_file', help='input fasta file', type=str, required=True)
    parser.add_argument('-d', '--debug', help='debugging', action='store_const', dest='loglevel', const=logging.DEBUG,
                        default=logging.INFO)

    args = parser.parse_args()

    logger.setLevel(args.loglevel)

    pf = processFasta(fasta_file=args.fasta_file)
    pf.process_fasta_file()
    results = pf.get_sequence_dict()
    for result in results:
        logging.info(result)
        logging.info(results[result])