import unittest
from tests.access_test_files import TestFiles
from adding_stats_to_mmcif.add_sequence_to_mmcif import ExtractFromMmcif


class TestGetDataFromMmcif(unittest.TestCase):

    def setUp(self):
        self.test_files = TestFiles()

    def test_extract_from_missing_mmcif(self):
        mm = ExtractFromMmcif(mmcif_file='missing file')
        sequence_dict = mm.get_sequence_dict()
        self.assertTrue(sequence_dict == dict())

    def test_extract_from_invalid_mmcif(self):
        mm = ExtractFromMmcif(mmcif_file=self.test_files.TEST_INVALID_MMCIF_FILE)
        sequence_dict = mm.get_sequence_dict()
        self.assertTrue(sequence_dict == dict())

    def test_get_non_standard_one_letter_ALA(self):
        mm = ExtractFromMmcif(mmcif_file=self.test_files.TEST_VALID_MMCIF_FILE)
        one_letter = mm.get_non_standard_one_letter(three_letter='ALA')
        self.assertTrue(one_letter == 'A')

    def test_get_non_standard_one_letter_TPO(self):
        mm = ExtractFromMmcif(mmcif_file=self.test_files.TEST_VALID_MMCIF_FILE)
        one_letter = mm.get_non_standard_one_letter(three_letter='TPO')
        self.assertTrue(one_letter == 'T')

    def test_get_non_standard_one_letter_SEP(self):
        mm = ExtractFromMmcif(mmcif_file=self.test_files.TEST_VALID_MMCIF_FILE)
        one_letter = mm.get_non_standard_one_letter(three_letter='SEP')
        self.assertTrue(one_letter == 'S')

    def test_get_non_standard_one_letter_MAN(self):
        mm = ExtractFromMmcif(mmcif_file=self.test_files.TEST_VALID_MMCIF_FILE)
        one_letter = mm.get_non_standard_one_letter(three_letter='MAN')
        self.assertTrue(one_letter == 'X')

    def test_get_data_from_3zt9(self):
        self.test_files.one_sequence()
        mm = ExtractFromMmcif(mmcif_file=self.test_files.cif)
        entity_dict = self.test_files.observed_seq
        sequence_dict = mm.get_sequence_dict()
        self.assertFalse(sequence_dict == dict())
        for entity_id in entity_dict:
            self.assertTrue(sequence_dict.get(entity_id, {}).get('sequence', '') == entity_dict[entity_id]['sequence'])
            self.assertTrue(sequence_dict.get(entity_id, {}).get('chains', []) == entity_dict[entity_id]['chains'])

    def test_get_data_from_5liz(self):
        self.test_files.five_sequences()
        mm = ExtractFromMmcif(mmcif_file=self.test_files.cif)
        entity_dict = self.test_files.observed_seq
        sequence_dict = mm.get_sequence_dict()
        self.assertFalse(sequence_dict == dict())
        for entity_id in entity_dict:
            entity_dict_chains = entity_dict[entity_id]['chains']
            chains = sequence_dict.get(entity_id, {}).get('chains', [])
            sequence = sequence_dict.get(entity_id, {}).get('sequence', '')
            sample_sequence = entity_dict[entity_id]['sequence']
            self.assertTrue(sequence == sample_sequence)
            self.assertTrue(sorted(chains) == sorted(entity_dict_chains))

    def test_get_data_from_6fqf(self):
        self.test_files.four_chains_one_polymer()
        mm = ExtractFromMmcif(mmcif_file=self.test_files.cif)
        entity_dict = self.test_files.observed_seq
        sequence_dict = mm.get_sequence_dict()
        self.assertFalse(sequence_dict == dict())
        for entity_id in entity_dict:
            chains = sequence_dict.get(entity_id, {}).get('chains', [])
            self.assertTrue(sequence_dict.get(entity_id, {}).get('sequence', '') == entity_dict[entity_id]['sequence'])
            self.assertTrue(sorted(chains) == sorted(entity_dict[entity_id]['chains']))


if __name__ == '__main__':
    unittest.main()
