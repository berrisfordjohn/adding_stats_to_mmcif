#!/usr/bin/env python
import logging
import argparse
from Bio import Align
from Bio import pairwise2
from Bio.SubsMat import MatrixInfo as matlist

logger = logging.getLogger()
FORMAT = "%(filename)s - %(funcName)s - %(message)s"
logging.basicConfig(format=FORMAT)

class SequenceAlign:

    def __init__(self, sequence1, sequence2):
        self.sequence1 = sequence1
        self.sequence2 = sequence2
        self.score = None
        self.alignment_result = list()
        self.alignment_result_target = list()
        self.alignment_result_query = list()
        logging.debug(self.sequence1)
        logging.debug(self.sequence2)

    def rna(self, seq):
        return set(seq).issubset(set("AUGC"))

    def dna(self, seq):
        return set(seq).issubset(set("ATGC"))

    # def dnarna(self, seq):
    #    return self.rna(seq=seq) or self.dna(seq=seq)

    def both_sequences_same_type(self):
        if self.dna(self.sequence1) == self.dna(self.sequence2) and self.rna(self.sequence1) == self.rna(
                self.sequence2):
            return True, ''
        return False, 'sequences not the same type'
        # if self.dnarna(self.sequence1) != self.dnarna(self.sequence2):
        #    return False, 'sequences not the same type'
        # return True, ''

    def remove_gaps(self, sequence):
        return str(sequence).replace("\n", "").replace(" ", "")

    def prepare_sequences(self):
        self.sequence1 = self.remove_gaps(self.sequence1)
        self.sequence2 = self.remove_gaps(self.sequence2)
        return self.both_sequences_same_type()

    def pairwise2(self):

        matrix = matlist.blosum62
        gap_open = -10
        gap_extend = -0.5
        alns = pairwise2.align.globalds(self.sequence1, self.sequence2, matrix, gap_open, gap_extend)[0]
        logging.info(pairwise2.format_alignment(*alns))
        logging.info(alns)
        self.score = alns[2]

    def pairwise_aligner(self):

        aligner = Align.PairwiseAligner()
        aligner.open_gap_score = -10
        aligner.extend_gap_score = -0.5
        aligner.target_end_gap_score = 0.0
        aligner.query_end_gap_score = 0.0
        # aligner.match = 2
        # aligner.mismatch = -1
        # only need to run aligner.score. This improves memory usage and speed.
        # logging.debug('length of query: {}'.format(len(self.sequence1)))
        # logging.debug('length of target: {}'.format(len(self.sequence2)))
        alignments = aligner.align(self.sequence1, self.sequence2)
        for alignment in sorted(alignments):
            self.alignment_result_query = list()
            self.alignment_result_target = list()
            logging.debug(alignment.score)
            current_query_position = 0
            current_target_position = 0

            for align_tupple in alignment.path:
                working_target_position = align_tupple[0]
                working_query_position = align_tupple[1]
                query_shift = working_query_position - current_query_position
                target_shift = working_target_position - current_target_position
                #  logging.debug('query shift: {}'.format(query_shift))
                #  logging.debug('target shift: {}'.format(target_shift))
                # expand the shift into a list. Then for each position add the position in the list to a dictionary?
                query_sequence = alignment.query[current_query_position:working_query_position]
                #  logging.debug('query sequence: {}'.format(query_sequence))
                target_sequence = alignment.target[current_target_position:working_target_position]
                #  logging.debug('target sequence: {}'.format(target_sequence))
                # need to account for insertions
                self.alignment_result_target.extend(list(target_sequence))
                if query_sequence:
                    query_sequence = list(query_sequence)
                elif target_sequence:
                    query_sequence = ['-'] * len(target_sequence)
                self.alignment_result_query.extend(query_sequence)

                current_target_position = working_target_position
                current_query_position = working_query_position

            logging.debug(self.alignment_result_target)
            logging.debug(self.alignment_result_query)

            self.score = alignment.score
            result = {'score': self.score, 'target_result': self.alignment_result_target,
                      'query_result': self.alignment_result_query}
            self.alignment_result.append(result)
        #align_score = aligner.score(self.sequence1, self.sequence2)
        logging.info(self.score)

    def get_alignment_score(self):
        return self.score

    def get_alignment_result(self):
        return self.alignment_result

    def do_sequences_align(self):
        if self.score > 0:
            return True
        return False

    def do_sequence_alignment(self):
        self.alignment_result = []
        sequences_ok, error = self.prepare_sequences()
        if not sequences_ok:
            return False, error, 0
        self.pairwise_aligner()
        if self.do_sequences_align():
            return True, '', self.score
        return False, 'sequences do not align', 0


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', help='debugging', action='store_const', dest='loglevel', const=logging.DEBUG,
                        default=logging.INFO)
    args = parser.parse_args()
    logger.setLevel(args.loglevel)

    test_sequences = [
        'MEKLEVGIYTRAREGEIACGDACLVKRVEGVIFLAVGDGIGHGPEAARAAEIAIASMESSMNTGLVNIFQLCHRELRGTRGAVAALCRVDRRQGLWQAAIVGNIHVKILSAKGIITPLATPGILGYNYPHQLLIAKGSYQEGDLFLIHSDGIQEGAVPLALLANYRLTAEELVRLIGEKYGRRDDDVAVIVAR',
        'TRAREGEIACGDACLVKRVEGVIFLAVGDGIGHGPEAARAAEIAIASMESSMNTGLVNIFQLCHRELRGTRGAVAALCRVDRRQGLWQAAIVGNIHVKILSAKGIITPLATPGILGYNYPHQLLIAKGSYQEGDLFLIHSDGIQEGAVPLALLANYRLTAEELVRLIGE',
        'DMEGYFVDE', 'RANDOM']

    for sequence in test_sequences:
        sa = SequenceAlign(sequence1=test_sequences[0], sequence2=sequence)
        aligned, error, score = sa.do_sequence_alignment()
        result_list = sa.get_alignment_result()
        logging.info('is aligned: {}'.format(aligned))
        logging.info('error: "{}"'.format(error))
        logging.info('score: {}'.format(score))
        logging.info('number of results: {}'.format(len(result_list)))
        logging.info(result_list)
