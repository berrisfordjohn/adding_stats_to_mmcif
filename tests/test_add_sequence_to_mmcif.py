import unittest
from tests.access_test_files import TestFiles
from adding_stats_to_mmcif.add_sequence_to_mmcif import AddSequenceToMmcif
from adding_stats_to_mmcif.cif_handling import mmcifHandling
import tempfile
import os
import shutil


class TestAddDataToMmcif(unittest.TestCase):

    def setUp(self):
        self.test_files = TestFiles()

    def test_get_entity_poly_five_sequences(self):

        self.test_files.five_sequences()
        sample_seq = self.test_files.sample_seq

        temp_dir = tempfile.mkdtemp()
        output_cif = os.path.join(temp_dir, 'output.cif')
        mm = AddSequenceToMmcif(input_mmcif=self.test_files.cif,
                                output_mmcif=output_cif,
                                fasta_file=self.test_files.fasta)
        worked = mm.process_data()
        self.assertTrue(worked)
        self.assertTrue(os.path.exists(output_cif))

        om = mmcifHandling(fileName=output_cif)
        entity_poly = om.getCategory('entity_poly')
        for cat in entity_poly:
            for instance, entity_id in enumerate(entity_poly[cat]['entity_id']):
                sequence = entity_poly[cat]['pdbx_seq_one_letter_code'][instance]
                sample_seq_key = self.test_files.sample_seq_to_obs_remapping[entity_id]
                self.assertTrue(sequence == sample_seq[sample_seq_key])

        shutil.rmtree(temp_dir)

    def test_get_entity_poly_three_sequences(self):

        self.test_files.three_sequences()
        sample_seq = self.test_files.sample_seq

        temp_dir = tempfile.mkdtemp()
        output_cif = os.path.join(temp_dir, 'output.cif')
        mm = AddSequenceToMmcif(input_mmcif=self.test_files.cif,
                                output_mmcif=output_cif,
                                fasta_file=self.test_files.fasta)
        worked = mm.process_data()
        self.assertTrue(worked)
        self.assertTrue(os.path.exists(output_cif))

        om = mmcifHandling(fileName=output_cif)
        entity_poly = om.getCategory('entity_poly')
        for cat in entity_poly:
            for instance, entity_id in enumerate(entity_poly[cat]['entity_id']):
                sequence = entity_poly[cat]['pdbx_seq_one_letter_code'][instance]
                sample_seq_key = self.test_files.sample_seq_to_obs_remapping[entity_id]
                self.assertTrue(sequence == sample_seq[sample_seq_key])

        shutil.rmtree(temp_dir)


if __name__ == '__main__':
    unittest.main()
