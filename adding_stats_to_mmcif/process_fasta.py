#!/usr/bin/env python
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC
import logging
import argparse
import os

logger = logging.getLogger()
FORMAT = "%(filename)s - %(funcName)s - %(message)s"
logging.basicConfig(format=FORMAT)


class ProcessFasta:

    def __init__(self, fasta_file):
        self.fasta_file = fasta_file
        self.fasta_data = None
        self.sequence_dict = dict()

    def process_fasta_file(self):
        if self.fasta_file:
            logging.debug('fasta file: {}'.format(self.fasta_file))
            if os.path.exists(self.fasta_file):
                logging.debug('processing fasta file')
                try:
                    self.fasta_data = SeqIO.parse(self.fasta_file, "fasta")
                    for record in self.fasta_data:
                        self.sequence_dict[record.id] = record.seq
                    return True
                except Exception as e:
                    logging.error('exception in reading fasta')
                    logging.error(e)
        return False

    def get_sequence_dict(self):
        return self.sequence_dict

    def write_fasta_file(self, sequence_dict):
        if not isinstance(sequence_dict, dict):
            logging.error('requires a dictionary')
            return False
        sequences = list()
        if sequence_dict:
            try:
                for key in sequence_dict:
                    record = SeqRecord(Seq(sequence_dict[key]), id=key)
                    sequences.append(record)
            except Exception as e:
                logging.error('exception is creating seq record iterator')
                logging.error(e)
                return False
            try:
                with open(self.fasta_file, 'w') as output_handle:
                    SeqIO.write(sequences, output_handle, "fasta")
                return True
            except Exception as e:
                logging.error('exception in writing fasta file')
                logging.error(e)
        return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fasta_file', help='input fasta file', type=str, required=True)
    parser.add_argument('-d', '--debug', help='debugging', action='store_const', dest='loglevel', const=logging.DEBUG,
                        default=logging.INFO)

    args = parser.parse_args()

    logger.setLevel(args.loglevel)

    pf = ProcessFasta(fasta_file=args.fasta_file)
    pf.process_fasta_file()
    results = pf.get_sequence_dict()
    for result in results:
        logging.info(result)
        logging.info(results[result])
