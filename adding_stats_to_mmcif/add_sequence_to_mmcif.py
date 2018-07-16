#!/usr/bin/env python
import os # pragma: no cover
from .cif_handling import mmcifHandling
from .process_fasta import processFasta
from pprint import pformat # pragma: no cover
import argparse # pragma: no cover
import logging # pragma: no cover
from .pairwise_align import SequenceAlign
from .get_data_from_pdbe_api import GetSpecificDataFromPdbeAPI

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
        self.non_standard_residue_mapping = dict()

    def get_sequence_dict(self):
        self.mm.parse_mmcif()
        self.get_seq_of_polymer_entities()
        self.get_data_from_atom_site()
        return self.sequence_dict

    def parse_mmcif(self):
        self.mm.parse_mmcif()

    def get_non_standard_one_letter(self, threeLetter):
        """
        Return the one letter code for a non standard residue.
        Checks the cache and then the PDBe API for the one letter code for a residue

        threeLetter = non standard residue three letter code
        returns the one letter code
        """
        if threeLetter in self.non_standard_residue_mapping:
            oneLetter = self.non_standard_residue_mapping[threeLetter]
        else:
            oneLetter = GetSpecificDataFromPdbeAPI().get_one_letter_code_for_compound(compound=threeLetter)
            self.non_standard_residue_mapping[threeLetter] = oneLetter
        return oneLetter

    def get_seq_of_polymer_entities(self):
        internal_dict = dict()
        if self.mm:
            row_list = self.mm.getCategoryList('entity_poly_seq')
            #logging.debug(row_list)
            for row in row_list:
                entity_id = row['entity_id']
                threeLetter = row['mon_id']
                num = row['num']
                hetero = row['hetero']

                if threeLetter in residue_map_3to1:
                    oneLetter = residue_map_3to1[threeLetter]
                else:
                    oneLetter = self.get_non_standard_one_letter(threeLetter=threeLetter)
                if hetero == 'n':
                    internal_dict.setdefault(entity_id, []).append(oneLetter)

        for entity_id in internal_dict:
            sequence_list = internal_dict[entity_id]
            sequence = ''.join(sequence_list)
            if sequence:
                self.sequence_dict.setdefault(entity_id, {})['sequence'] = sequence

    def get_data_from_atom_site(self):
        atom_site_dict = dict()
        sequence_dict = dict()
        if self.mm:
            row_list = self.mm.getCategoryList('atom_site')
            for row in row_list:
                entity_id = row['label_entity_id']
                chain_id = row['auth_asym_id']
                threeLetter = row['auth_comp_id']
                residue_number = row['auth_seq_id']
                ins_code = row['pdbx_PDB_ins_code']
                group_PDB = row['group_PDB']

                if threeLetter in residue_map_3to1:
                    oneLetter = residue_map_3to1[threeLetter]
                else:
                    oneLetter = 'X'

                # TODO is this right? Can this be relied upon?
                if group_PDB == 'ATOM':
                    #logging.debug('{} {}{} {}'.format(entity_id, chain_id, residue_number, oneLetter))
                    atom_site_dict.setdefault(entity_id, {}).setdefault(chain_id, [])
                    if residue_number not in atom_site_dict[entity_id][chain_id]:
                        #logging.debug('new residue')
                        sequence_dict.setdefault(entity_id, {}).setdefault(chain_id, []).append(oneLetter)
                        atom_site_dict[entity_id][chain_id].append(residue_number)

        logging.debug('atom site dict: {}'.format(atom_site_dict))
        logging.debug('sequence dict: {}'.format(sequence_dict))
        for entity_id in sequence_dict:
            for chain_id in sequence_dict[entity_id]:
                if chain_id not in self.sequence_dict.setdefault(entity_id, {}).setdefault('chains', []):
                    self.sequence_dict.setdefault(entity_id, {}).setdefault('chains', []).append(chain_id)
                if 'sequence' not in self.sequence_dict[entity_id]:
                    oneLetterSequence = ''.join(sequence_dict[entity_id][chain_id])
                    self.sequence_dict[entity_id]['sequence'] = oneLetterSequence
                

    def remove_category(self, category):
        self.mm.removeCategory(category=category)

    def add_to_mmcif(self, category, item_value_dict, ordinal=None):
        category_dict = self.mm.addValuesToCategory(category=category, item_value_dictionary=item_value_dict, ordinal_item=ordinal)
        self.mm.addToCif(category_dict)

    def write_mmcif(self, filename):
        self.mm.writeCif(fileName=filename)

class AddSequenceToMmcif:

    def __init__(self, input_mmcif, output_mmcif, fasta_file=None, input_sequence=None, input_chainids=None):
        self.input_mmcif = input_mmcif
        self.output_cif = output_mmcif
        self.fasta_file = fasta_file
        self.input_sequence = input_sequence
        self.input_chain_ids = input_chainids
        self.fasta_data = None
        self.input_sequence_dict = dict()
        self.mmcif_sequence_dict = dict()
        self.mmcif = None


    def process_fasta(self):
        if self.fasta_file:
            pf = processFasta(fasta_file=self.fasta_file)
            pf.process_fasta_file()
            self.input_sequence_dict = pf.get_sequence_dict()
            
    def process_sequence(self):
        if self.input_sequence and self.input_chain_ids:
            logging.debug('processing sequence')
            chain_ids = self.input_chain_ids.split(',')
            for chain in chain_ids:
                self.input_sequence_dict[chain] = self.input_sequence

    def prcocess_mmcif(self):
        logging.debug('processing {}'.format(self.input_mmcif))
        if os.path.exists(self.input_mmcif):
            self.mmcif = ExtractFromMmcif(mmcif_file=self.input_mmcif)
            self.mmcif_sequence_dict = self.mmcif.get_sequence_dict()
        logging.debug(self.mmcif_sequence_dict)

    def get_best_match(self, mmcif_sequence):
        best_score = 0
        best_seq = None
        for seq in self.input_sequence_dict:
            test_sequence = self.input_sequence_dict[seq]
            if len(test_sequence) >= len(mmcif_sequence):
                sa = SequenceAlign(sequence1=mmcif_sequence, sequence2=test_sequence)
                aligned, error, score = sa.do_sequence_alignment()
                if aligned:
                    if score > best_score:
                        best_seq = test_sequence
                        score = best_score
        return best_seq, best_score
        

    def match_sequences(self):
        mmcif_out = []
        logging.debug('mmcif sequences: {}'.format(self.mmcif_sequence_dict))
        logging.debug('input sequences: {}'.format(self.input_sequence_dict))
        for entity_id in self.mmcif_sequence_dict:
            if 'sequence' in self.mmcif_sequence_dict[entity_id]:
                mmcif_sequence = self.mmcif_sequence_dict[entity_id]['sequence']
                chain_ids = self.mmcif_sequence_dict[entity_id]['chains']
                logging.debug(chain_ids)

                matched_sequence, matched_score = self.get_best_match(mmcif_sequence=mmcif_sequence)
                if matched_sequence:
                    mmcif_out.append({'entity_id': entity_id, 
                                    'pdbx_seq_one_letter_code': matched_sequence,
                                    'pdbx_strand_id': ','.join(chain_ids)})


        if mmcif_out:
            logging.debug('adding data to mmcif: {}'.format(mmcif_out))
            mmcif_dict = {'entity_poly': mmcif_out}
            #self.mmcif.remove_category(category='entity_poly')
            self.add_to_mmcif(mmcif_dict=mmcif_dict)
            self.mmcif.write_mmcif(filename=self.output_cif)
        else:
            logging.debug('no sequence to add to mmcif')


    def add_to_mmcif(self, mmcif_dict):
        logging.debug(mmcif_dict)
        for cat in mmcif_dict:
            for row in mmcif_dict[cat]:
                logging.debug(row)
                self.mmcif.add_to_mmcif(category=cat, item_value_dict=row)


    def process_data(self):
        self.process_fasta()
        self.process_sequence()
        logging.debug(self.input_sequence_dict)
        if not self.input_sequence_dict:
            logging.error('missing input sequence')
            return False

        self.prcocess_mmcif()

        if not self.mmcif_sequence_dict and self.input_sequence_dict:
            logging.error('missing sequence from mmcif')
            return False

        self.match_sequences()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--output_mmcif', help='output mmcif file', type=str, required=True)
    parser.add_argument('--input_mmcif', help='input mmcif file', type=str, required=True)
    parser.add_argument('--fasta_file', help='input fasta file', type=str)
    parser.add_argument('--sequence', help='input sequence in one letter format', type=str)
    parser.add_argument('--chain_ids', help='input chain ids in a comma separated list', type=str)
    parser.add_argument('-d', '--debug', help='debugging', action='store_const', dest='loglevel', const=logging.DEBUG,
                        default=logging.INFO)

    args = parser.parse_args()

    logger.setLevel(args.loglevel)

    worked = AddSequenceToMmcif(input_mmcif=args.input_mmcif, 
                                output_mmcif=args.output_mmcif, 
                                fasta_file=args.fasta_file, 
                                input_sequence=args.sequence, 
                                input_chainids=args.chain_ids).process_data()