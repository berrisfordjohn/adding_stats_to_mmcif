import unittest
import tempfile
import shutil
import os
from adding_stats_to_mmcif.process_fasta import ProcessFasta
from tests.access_test_files import TestFiles


class TestProcessFasta(unittest.TestCase):

    def setUp(self):
        self.test_files = TestFiles()

    def test_missing_file(self):
        pf = ProcessFasta(fasta_file='missing_file.fasta')
        pf.process_fasta_file()
        data = pf.get_sequence_dict()
        self.assertEqual(data, dict())

    def test_invalid_fasta(self):
        pf = ProcessFasta(fasta_file=self.test_files.TEST_INVALID_FASTA_ONE_SEQUENCE)
        pf.process_fasta_file()
        data = pf.get_sequence_dict()
        self.assertEqual(data, dict())

    def test_valid_file_one_sequence(self):
        self.test_files.one_sequence()
        expected_result = self.test_files.sample_seq
        pf = ProcessFasta(fasta_file=self.test_files.fasta)
        pf.process_fasta_file()
        data = pf.get_sequence_dict()
        self.assertTrue(len(data.keys()) == 1)
        for key in data:
            self.assertTrue(key in expected_result)
            self.assertTrue(data[key] == expected_result[key])

    def test_invalid_file_one_sequence(self):
        pf = ProcessFasta(fasta_file=self.test_files.TEST_INVALID_FASTA_ONE_SEQUENCE)
        pf.process_fasta_file()
        data = pf.get_sequence_dict()
        self.assertEqual(data, dict())

    def test_valid_file_three_sequences(self):
        self.test_files.three_sequences()
        expected_result = self.test_files.sample_seq
        pf = ProcessFasta(fasta_file=self.test_files.fasta)
        pf.process_fasta_file()
        data = pf.get_sequence_dict()
        self.assertTrue(len(data.keys()) == 3)
        for key in data:
            self.assertTrue(key in expected_result)
            self.assertTrue(data[key] == expected_result[key])

    def test_valid_file_five_sequences(self):
        self.test_files.five_sequences()
        expected_result = self.test_files.sample_seq
        pf = ProcessFasta(fasta_file=self.test_files.fasta)
        pf.process_fasta_file()
        data = pf.get_sequence_dict()
        self.assertTrue(len(data.keys()) == 5)
        for key in data:
            self.assertTrue(key in expected_result)
            self.assertTrue(data[key] == expected_result[key])

    def test_write_valid_fasta(self):
        test = dict()
        test[
            'protein_a'] = 'MEGERKNNNKRWYFTREQLENSPSRRFGVDPDKELSYRQQAANLLQDMGQRLNVSQLTINTAIVYMHRFYMIQSFTQFPGNSVAPAALFLAAKVEEQPKKLEHVIKVAHTCLHPQESLPDTRSEAYLQQVQDLVILESIILQTLGFELTIDHPHTHVVKCTQLVRASKDLAQTSYFMATNSLHLTTFSLQYTPPVVACVCIHLACKWSNWEIPVSTDGKHWWEYVDATVTLELLDELTHEFLQILEKTPNRLKRIWNWRACEAA'
        test['RNA'] = 'AGAUCUGAGCCUGGGAGCUCUCU'
        temp_dir = tempfile.mkdtemp()
        output_fasta = os.path.join(temp_dir, 'output.fasta')
        pf = ProcessFasta(fasta_file=output_fasta)
        worked = pf.write_fasta_file(sequence_dict=test)
        self.assertTrue(worked)
        self.assertTrue(os.path.exists(output_fasta))

        shutil.rmtree(temp_dir)

    def test_write_invalid_fasta(self):
        test = []
        temp_dir = tempfile.mkdtemp()
        output_fasta = os.path.join(temp_dir, 'output.fasta')
        pf = ProcessFasta(fasta_file=output_fasta)
        worked = pf.write_fasta_file(sequence_dict=test)
        self.assertFalse(worked)
        self.assertFalse(os.path.exists(output_fasta))

        shutil.rmtree(temp_dir)


if __name__ == '__main__':
    unittest.main()
