import unittest
from adding_stats_to_mmcif.process_fasta import processFasta
from tests.access_test_files import TestFiles


class TestProcessFasta(unittest.TestCase):

    def setUp(self):
        self.test_files = TestFiles()

    def test_missing_file(self):
        pf = processFasta(fasta_file='missing_file.fasta')
        pf.process_fasta_file()
        data = pf.get_sequence_dict()
        self.assertEqual(data, dict())

    def test_valid_file_one_sequence(self):
        pf = processFasta(fasta_file=self.test_files.TEST_VALID_FASTA_ONE_SEQUENCE)
        pf.process_fasta_file()
        data = pf.get_sequence_dict()
        self.assertTrue(len(data.keys()) == 1)

    def test_invalid_file_one_sequence(self):
        pf = processFasta(fasta_file=self.test_files.TEST_INVALID_FASTA_ONE_SEQUENCE)
        pf.process_fasta_file()
        data = pf.get_sequence_dict()
        self.assertEqual(data, dict())

    def test_valid_file_three_sequences(self):
        pf = processFasta(fasta_file=self.test_files.TEST_VALID_FASTA_THREE_SEQUENCES)
        pf.process_fasta_file()
        data = pf.get_sequence_dict()
        self.assertTrue(len(data.keys()) == 3)


if __name__ == '__main__': # pragma: no cover
    unittest.main()