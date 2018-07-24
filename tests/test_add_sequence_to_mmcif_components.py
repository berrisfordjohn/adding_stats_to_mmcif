import unittest
from tests.access_test_files import TestFiles
from adding_stats_to_mmcif.add_sequence_to_mmcif import AddSequenceToMmcif
import tempfile
import shutil
import os


class TestAddDataToMmcif(unittest.TestCase):

    def setUp(self):
        self.test_files = TestFiles()

    def test_get_data_from_3zt9_via_AddSequenceToMmcif(self):
        self.test_files.one_sequence()
        mm = AddSequenceToMmcif(input_mmcif=self.test_files.cif,
                                output_mmcif='output.cif')
        entity_dict = self.test_files.observed_seq
        sequence_dict = mm.process_mmcif()
        self.assertFalse(sequence_dict == dict())
        for entity_id in entity_dict:
            self.assertTrue(sequence_dict.get(entity_id, {}).get('sequence', '') == entity_dict[entity_id]['sequence'])
            self.assertTrue(sequence_dict.get(entity_id, {}).get('chains', []) == entity_dict[entity_id]['chains'])

    def test_get_data_from_6fqf_via_AddSequenceToMmcif(self):
        self.test_files.four_chains_one_polymer()
        mm = AddSequenceToMmcif(input_mmcif=self.test_files.cif,
                                output_mmcif='output.cif')
        entity_dict = self.test_files.observed_seq
        sequence_dict = mm.process_mmcif()
        self.assertFalse(sequence_dict == dict())
        for entity_id in entity_dict:
            chains = sequence_dict.get(entity_id, {}).get('chains', [])
            self.assertTrue(sequence_dict.get(entity_id, {}).get('sequence', '') == entity_dict[entity_id]['sequence'])
            self.assertTrue(sorted(chains) == sorted(entity_dict[entity_id]['chains']))

    def test_get_data_from_5liz_via_AddSequenceToMmcif(self):
        self.test_files.five_sequences()
        mm = AddSequenceToMmcif(input_mmcif=self.test_files.cif,
                                output_mmcif='output.cif')
        entity_dict = self.test_files.observed_seq
        sequence_dict = mm.process_mmcif()
        self.assertFalse(sequence_dict == dict())
        for entity_id in entity_dict:
            chains = sequence_dict.get(entity_id, {}).get('chains', [])
            self.assertTrue(sequence_dict.get(entity_id, {}).get('sequence', '') == entity_dict[entity_id]['sequence'])
            self.assertTrue(sorted(chains) == sorted(entity_dict[entity_id]['chains']))

    def test_process_fasta_one_chain(self):

        self.test_files.one_sequence()
        expected_result = self.test_files.sample_seq
        mm = AddSequenceToMmcif(input_mmcif='input.cif', output_mmcif='output.cif',
                                fasta_file=self.test_files.fasta)
        data = mm.process_input_sequences()
        self.assertTrue(len(data.keys()) == 1)
        for key in data:
            self.assertTrue(key in expected_result)
            self.assertTrue(data[key] == expected_result[key])

    def test_process_fasta_five_chains(self):
        self.test_files.five_sequences()
        expected_result = self.test_files.sample_seq

        mm = AddSequenceToMmcif(input_mmcif='input.cif', output_mmcif='output.cif',
                                fasta_file=self.test_files.fasta)
        data = mm.process_input_sequences()
        self.assertTrue(len(data.keys()) == 5)
        for key in data:
            self.assertTrue(key in expected_result)
            self.assertTrue(data[key] == expected_result[key])

    def test_missing_fasta_file(self):
        mm = AddSequenceToMmcif(input_mmcif='input.cif', output_mmcif='output.cif',
                                fasta_file='missing_file.fasta')
        data = mm.process_input_sequences()
        self.assertEqual(data, dict())
        self.assertTrue(len(data.keys()) == 0)

    def test_invalid_fasta_file(self):
        mm = AddSequenceToMmcif(input_mmcif='input.cif', output_mmcif='output.cif',
                                fasta_file=self.test_files.TEST_INVALID_FASTA_ONE_SEQUENCE)
        data = mm.process_input_sequences()
        self.assertEqual(data, dict())
        self.assertTrue(len(data.keys()) == 0)

    def test_process_sequence_two_chains(self):

        sequence = 'MEKLEVGIYTRAREGEIACGDACLVKRVEGVIFLAVGDGIGHGPEAARAAEIAIASMESSMNTGLVNIFQLCHRELRGTRGAVAALCRVDRRQGLWQAAIVGNIHVKILSAKGIITPLATPGILGYNYPHQLLIAKGSYQEGDLFLIHSDGIQEGAVPLALLANYRLTAEELVRLIGEKYGRRDDDVAVIVAR'
        chains = 'A,B'
        mm = AddSequenceToMmcif(input_mmcif='input.cif', output_mmcif='output.cif', input_chainids=chains,
                                input_sequence=sequence)
        data = mm.process_input_sequences()
        self.assertTrue(len(data.keys()) == 2)
        for key in data:
            self.assertTrue(key in chains.split(','))
            self.assertTrue(data[key] == sequence)

    def test_get_data_from_3zt9_via_AddSequenceToMmcif_process_data(self):
        self.test_files.one_sequence()
        test_dir = tempfile.mkdtemp()
        output_cif = os.path.join(test_dir, 'output.cif')
        mm = AddSequenceToMmcif(input_mmcif=self.test_files.cif,
                                output_mmcif=output_cif,
                                fasta_file=self.test_files.fasta)
        worked = mm.process_data()
        self.assertTrue(worked)
        shutil.rmtree(test_dir)

    def test_get_data_from_3zt9_via_AddSequenceToMmcif_get_best_match(self):
        self.test_files.one_sequence()
        expected_result = self.test_files.sample_seq['pdb|3zt9|A']
        entity_dict = self.test_files.observed_seq

        mm = AddSequenceToMmcif(input_mmcif=self.test_files.cif,
                                output_mmcif='output.cif',
                                fasta_file=self.test_files.fasta)
        mm.process_input_sequences()
        best_seq, best_score = mm.get_best_match(mmcif_sequence=entity_dict['1']['sequence'])
        self.assertTrue(best_seq == expected_result)
        self.assertTrue(best_score > 0)


if __name__ == '__main__':
    unittest.main()
