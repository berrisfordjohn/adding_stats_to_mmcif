#!/usr/bin/env python
import os
from .cif_handling import mmcifHandling
import argparse
import logging

logger = logging.getLogger()
FORMAT = "%(filename)s - %(funcName)s - %(message)s"
logging.basicConfig(format=FORMAT)

residue_map_1to3 = {
    'A': 'ALA', 'C': 'CYS', 'D': 'ASP', 'E': 'GLU', 'F': 'PHE', 'G': 'GLY',\
    'H': 'HIS', 'I': 'ILE', 'K': 'LYS', 'L': 'LEU', 'M': 'MET', 'N': 'ASN',\
    'P': 'PRO', 'Q': 'GLN', 'R': 'ARG', 'S': 'SER', 'T': 'THR', 'V': 'VAL',\
    'W': 'TRP', 'Y': 'TYR',
}

residue_map_3to1 = {v: k for k, v in residue_map_1to3.items()}
residue_map_3to1['A'] = 'A'
residue_map_3to1['G'] = 'G'
residue_map_3to1['C'] = 'C'
residue_map_3to1['T'] = 'T'
residue_map_3to1['U'] = 'U'

class ExtractFromMmcif():

    def __init__(self, mmcif_file):
        self.mmcif_file = mmcif_file
        self.mm = mmcifHandling(fileName=self.mmcif_file)
        self.sequence_dict = dict()

    def get_sequence_dict(self):
        self.mm.parse_mmcif()
        self.get_seq_of_polymer_entities()
        self.get_chain_id_per_entity()
        return self.sequence_dict

    def parse_mmcif(self):
        self.mm.parse_mmcif()

    def get_seq_of_polymer_entities(self):
        if self.mm:
            row_list = self.mm.getCategoryList('entity_poly_seq')
            for row in row_list:
                entity_id = row['entity_id']
                threeLetter = row['mon_id']
                num = row['num']
                hetero = row['hetero']

                if threeLetter in residue_map_3to1:
                    oneLetter = residue_map_3to1[threeLetter]
                else:
                    oneLetter = 'X'
                if hetero == 'n':
                    self.sequence_dict.setdefault(entity_id, {}).setdefault('sequence', []).append(oneLetter)

    def get_chain_id_per_entity(self):
        if self.mm:
            row_list = self.mm.getCategoryList('atom_site')
            for row in row_list:
                entity_id = row['label_entity_id']
                chain_id = row['auth_asym_id']
                if chain_id not in self.sequence_dict.setdefault(entity_id, {}).setdefault('chains', []):
                    self.sequence_dict.setdefault(entity_id, {}).setdefault('chains', []).append(chain_id)


class AddSequenceToMmcif:

    def __init__(self, input_mmcif, output_mmcif, fasta_file):
        self.input_mmcif = input_mmcif
        self.output_cif = output_mmcif
        self.fasta_file = fasta_file
        self.fasta_sequence_list = list()
        self.mmcif_sequence_dict = dict()

    def process_fasta(self):
        if os.path.exists(self.fasta_file):
            pass

    def prcocess_mmcif(self):
        if os.path.exists(self.input_mmcif):
            self.mmcif_sequence_dict = ExtractFromMmcif(mmcif_file=self.input_mmcif).get_sequence_dict()

    



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