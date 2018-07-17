import unittest
from tests.access_test_files import TestFiles
from adding_stats_to_mmcif.add_sequence_to_mmcif import ExtractFromMmcif, AddSequenceToMmcif


class TestAddDataFromMmcif(unittest.TestCase):

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

    def test_extract_from_valid_mmcif(self):
        entity_1_seq = 'MEKLEVGIYTRAREGEIACGDACLVKRVEGVIFLAVGDGIGHGPEAARAAEIAIASMESSMNTGLVNIFQLCHRELRGTRGAVAALCRVDRRQGLWQAAIVGNIHVKILSAKGIITPLATPGILGYNYPHQLLIAKGSYQEGDLFLIHSDGIQEGAVPLALLANYRLTAEELVRLIGEKYGRRDDDVAVIVAR'
        entity_1_chains = ['A']
        mm = ExtractFromMmcif(mmcif_file=self.test_files.TEST_VALID_MMCIF_FILE)
        sequence_dict = mm.get_sequence_dict()
        self.assertFalse(sequence_dict == dict())
        self.assertTrue(sequence_dict.get('1', {}).get('sequence', '') == entity_1_seq)
        self.assertTrue(sequence_dict.get('1', {}).get('chains', '') == entity_1_chains)


if __name__ == '__main__':
    unittest.main()
