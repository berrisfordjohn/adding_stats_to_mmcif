#!/usr/bin/env python
import os
from .cif_handling import mmcifHandling
from .process_fasta import ProcessFasta
import argparse
import logging
from .pairwise_align import SequenceAlign
from .get_data_from_pdbe_api import GetSpecificDataFromPdbeAPI

logger = logging.getLogger()
FORMAT = "%(filename)s - %(funcName)s - %(message)s"
logging.basicConfig(format=FORMAT)

residue_map_1to3 = {
    'A': 'ALA', 'C': 'CYS', 'D': 'ASP', 'E': 'GLU', 'F': 'PHE', 'G': 'GLY',
    'H': 'HIS', 'I': 'ILE', 'K': 'LYS', 'L': 'LEU', 'M': 'MET', 'N': 'ASN',
    'P': 'PRO', 'Q': 'GLN', 'R': 'ARG', 'S': 'SER', 'T': 'THR', 'V': 'VAL',
    'W': 'TRP', 'Y': 'TYR',
}

residue_map_3to1 = {v: k for k, v in residue_map_1to3.items()}
residue_map_3to1['A'] = 'A'
residue_map_3to1['G'] = 'G'
residue_map_3to1['C'] = 'C'
residue_map_3to1['T'] = 'T'
residue_map_3to1['U'] = 'U'


class ExtractFromMmcif:

    def __init__(self, mmcif_file):
        self.mmcif_file = mmcif_file
        self.mm = mmcifHandling(fileName=self.mmcif_file)
        self.sequence_dict = dict()
        self.non_standard_residue_mapping = dict()

    def get_sequence_dict(self):
        parsed = self.parse_mmcif()
        if parsed:
            self.get_seq_of_polymer_entities()
            self.get_data_from_atom_site()
        return self.sequence_dict

    def parse_mmcif(self):
        parsed = self.mm.parse_mmcif()
        return parsed

    def get_one_letter_code(self, three_letter):
        if three_letter in residue_map_3to1:
            one_letter = residue_map_3to1[three_letter]
        else:
            one_letter = self.get_non_standard_one_letter(three_letter=three_letter)
        return one_letter

    def get_non_standard_one_letter(self, three_letter):
        """
        Return the one letter code for a non standard residue.
        Checks the cache and then the PDBe API for the one letter code for a residue

        threeLetter = non standard residue three letter code
        returns the one letter code
        """
        if three_letter in self.non_standard_residue_mapping:
            one_letter = self.non_standard_residue_mapping[three_letter]
        else:
            one_letter = GetSpecificDataFromPdbeAPI().get_one_letter_code_for_compound(compound=three_letter)
            self.non_standard_residue_mapping[three_letter] = one_letter
        return one_letter

    def get_seq_of_polymer_entities(self):
        internal_dict = dict()
        if self.mm:
            row_list = self.mm.getCategoryList('entity_poly_seq')
            # logging.debug(row_list)
            for row in row_list:
                entity_id = row['entity_id']
                three_letter = row['mon_id']
                num = row['num']
                hetero = row['hetero']

                one_letter = self.get_one_letter_code(three_letter=three_letter)
                # if hetero == 'n': # hetero is used for a heterogen instead of microhet in refmac.
                internal_dict.setdefault(entity_id, []).append(one_letter)

        logging.debug('internal_dict: {}'.format(internal_dict))
        for entity_id in internal_dict:
            sequence_list = internal_dict[entity_id]
            sequence = ''.join(sequence_list)
            if sequence:
                self.sequence_dict.setdefault(entity_id, {})['sequence'] = sequence

    def get_data_from_atom_site(self):
        atom_site_dict = dict()
        atom_site_sequence_dict = dict()
        if self.mm:
            row_list = self.mm.getCategoryList('atom_site')
            for row in row_list:
                entity_id = row['label_entity_id']
                chain_id = row['auth_asym_id']
                three_letter = row['auth_comp_id']
                residue_number = row['auth_seq_id']
                ins_code = row['pdbx_PDB_ins_code']
                group_PDB = row['group_PDB']

                one_letter = self.get_one_letter_code(three_letter=three_letter)

                # logging.debug('{} {}{} {}'.format(entity_id, chain_id, residue_number, one_letter))
                atom_site_dict.setdefault(entity_id, {}).setdefault(chain_id, [])
                if residue_number not in atom_site_dict[entity_id][chain_id]:
                    # logging.debug('new residue')
                    atom_site_sequence_dict.setdefault(entity_id, {}).setdefault(chain_id, []).append(one_letter)
                    atom_site_dict[entity_id][chain_id].append(residue_number)

        logging.debug('atom site dict: {}'.format(atom_site_dict))
        logging.debug('sequence dict: {}'.format(atom_site_sequence_dict))
        for entity_id in atom_site_sequence_dict:
            for chain_id in atom_site_sequence_dict[entity_id]:
                if entity_id in self.sequence_dict:
                    if 'sequence' in self.sequence_dict[entity_id]:
                        self.sequence_dict.setdefault(entity_id, {}).setdefault('chains', []).append(chain_id)
                        one_letter_sequence = ''.join(atom_site_sequence_dict[entity_id][chain_id])
                        self.sequence_dict.setdefault(entity_id, {})['sequence'] = one_letter_sequence

    def remove_category(self, category):
        self.mm.removeCategory(category=category)

    def add_to_mmcif(self, category, item_value_dict, ordinal=None):
        category_dict = self.mm.addValuesToCategory(category=category, item_value_dictionary=item_value_dict,
                                                    ordinal_item=ordinal)
        self.mm.addToCif(category_dict)

    def add_exptl(self):
        exptl_data = self.mm.addExptlToCif()
        if exptl_data:
            return True
        return False

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

    def process_input_sequences(self):
        if self.fasta_file and self.input_sequence:
            logging.error('both input fasta and input sequence provided. Please only provide one')
            return False
        ok = self.process_fasta()
        ok = self.process_sequence()
        return self.input_sequence_dict

    def process_fasta(self):
        if self.fasta_file:
            pf = ProcessFasta(fasta_file=self.fasta_file)
            pf.process_fasta_file()
            self.input_sequence_dict = pf.get_sequence_dict()
            if self.input_sequence_dict:
                logging.debug(self.input_sequence_dict)
                return True
        return False

    def process_sequence(self):
        if self.input_sequence and self.input_chain_ids:
            logging.debug('processing sequence')
            chain_ids = self.input_chain_ids.split(',')
            for chain in chain_ids:
                self.input_sequence_dict[chain] = self.input_sequence
            if self.input_sequence_dict:
                logging.debug(self.input_sequence_dict)
                return True
        return False

    def process_mmcif(self):
        logging.debug('processing {}'.format(self.input_mmcif))
        if os.path.exists(self.input_mmcif):
            self.mmcif = ExtractFromMmcif(mmcif_file=self.input_mmcif)
            self.mmcif_sequence_dict = self.mmcif.get_sequence_dict()
        logging.debug(self.mmcif_sequence_dict)
        return self.mmcif_sequence_dict

    def get_best_match(self, mmcif_sequence):
        best_score = 0
        best_seq = None
        for seq in self.input_sequence_dict:
            test_sequence = self.input_sequence_dict[seq]
            logging.debug(test_sequence)
            if len(test_sequence) >= len(mmcif_sequence):
                sa = SequenceAlign(sequence1=mmcif_sequence, sequence2=test_sequence)
                aligned, error, score = sa.do_sequence_alignment()
                if aligned:
                    if score > best_score:
                        best_seq = test_sequence
                        best_score = score
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
            # self.mmcif.remove_category(category='entity_poly')
            self.add_to_mmcif(mmcif_dict=mmcif_dict)
            self.add_exptl()
            self.mmcif.write_mmcif(filename=self.output_cif)
            if os.path.exists(self.output_cif):
                return True
        else:
            logging.debug('no sequence to add to mmcif')
        return False

    def add_to_mmcif(self, mmcif_dict):
        logging.debug(mmcif_dict)
        for cat in mmcif_dict:
            for row in mmcif_dict[cat]:
                logging.debug(row)
                self.mmcif.add_to_mmcif(category=cat, item_value_dict=row)

    def add_exptl(self):
        return self.mmcif.add_exptl()

    def process_data(self):
        self.process_input_sequences()
        logging.debug(self.input_sequence_dict)
        if not self.input_sequence_dict:
            logging.error('missing input sequence')
            return False

        self.process_mmcif()

        if not self.mmcif_sequence_dict and self.input_sequence_dict:
            logging.error('missing sequence from mmcif')
            return False

        return self.match_sequences()


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
