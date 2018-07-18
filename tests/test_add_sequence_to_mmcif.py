import unittest
from tests.access_test_files import TestFiles
from adding_stats_to_mmcif.add_sequence_to_mmcif import AddSequenceToMmcif
from adding_stats_to_mmcif.cif_handling import mmcifHandling
from adding_stats_to_mmcif.process_fasta import ProcessFasta
import tempfile
import os


class TestAddDataToMmcif(unittest.TestCase):

    def setUp(self):
        self.test_files = TestFiles()

    def test_get_entity_poly_for_5l1z(self):
        self.test_files.five_sequences()
        entity_dict = self.test_files.observed_seq

        sequence_dict = dict()
        for key in entity_dict:
            sequence_dict[key] = entity_dict[key]['sequence']

        temp_dir = tempfile.mkdtemp()
        fasta_file = os.path.join(temp_dir, 'input.fasta')
        pf = ProcessFasta(fasta_file=fasta_file)
        worked = pf.write_fasta_file(sequence_dict=sequence_dict)
        self.assertTrue(worked)

        output_cif = os.path.join(temp_dir, 'output.cif')
        mm = AddSequenceToMmcif(input_mmcif=self.test_files.cif,
                                output_mmcif=output_cif,
                                fasta_file=self.test_files.fasta)
        worked = mm.process_data()
        self.assertTrue(worked)
        self.assertTrue(os.path.exists(output_cif))

        om = mmcifHandling(fileName=output_cif)
        entity_poly = om.getCategory('entity_poly')


if __name__ == '__main__':
    unittest.main()
