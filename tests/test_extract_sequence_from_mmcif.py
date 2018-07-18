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
        one_letter = mm.get_non_standard_one_letter(threeLetter='ALA')
        self.assertTrue(one_letter == 'A')

    def test_get_non_standard_one_letter_TPO(self):
        mm = ExtractFromMmcif(mmcif_file=self.test_files.TEST_VALID_MMCIF_FILE)
        one_letter = mm.get_non_standard_one_letter(threeLetter='TPO')
        self.assertTrue(one_letter == 'T')

    def test_get_non_standard_one_letter_SEP(self):
        mm = ExtractFromMmcif(mmcif_file=self.test_files.TEST_VALID_MMCIF_FILE)
        one_letter = mm.get_non_standard_one_letter(threeLetter='SEP')
        self.assertTrue(one_letter == 'S')

    def test_get_non_standard_one_letter_MAN(self):
        mm = ExtractFromMmcif(mmcif_file=self.test_files.TEST_VALID_MMCIF_FILE)
        one_letter = mm.get_non_standard_one_letter(threeLetter='MAN')
        self.assertTrue(one_letter == 'X')

    def test_get_data_from_3zt9(self):
        mm = ExtractFromMmcif(mmcif_file=self.test_files.TEST_VALID_MMCIF_FILE)
        entity_dict = dict()
        entity_dict['1'] = {
            'sequence': 'EKLEVGIYTRAREGEIACGDACLVKRVEGVIFLAVGDGIGHGPEAARAAEIAIASMESSMNTGLVNIFQLCHRELRGTRGAVAALCRVDRRQGLWQAAIVGNIHVKILSAKGIITPLATPGILGYNYPHQLLIAKGSYQEGDLFLIHSDGIQEGAVPLALLANYRLTAEELVRLIGEKYGRRDDDVAVIVAR',
            'chains': ['A']}
        sequence_dict = mm.get_sequence_dict()
        self.assertFalse(sequence_dict == dict())
        for entity_id in entity_dict:
            self.assertTrue(sequence_dict.get(entity_id, {}).get('sequence', '') == entity_dict[entity_id]['sequence'])
            self.assertTrue(sequence_dict.get(entity_id, {}).get('chains', []) == entity_dict[entity_id]['chains'])

    def test_get_data_from_5liz(self):
        mm = ExtractFromMmcif(mmcif_file=self.test_files.TEST_VALID_5l1z_FIVE_POLYMERS_WITH_TPO_AND_RNA_MMCIF_FILE)
        entity_dict = dict()
        entity_dict['2'] = {
            'sequence': 'NNNKRWYFTREQLENSPSRRFGVDPDKELSYRQQAANLLQDMGQRLNVSQLTINTAIVYMHRFYMIQSFTQFPGNSVAPAALFLAAKVEEQPKKLEHVIKVAHTCLHPQESLPDTRSEAYLQQVQDLVILESIILQTLGFELTIDHPHTHVVKCTQLVRASKDLAQTSYFMATNSLHLTTFSLQYTPPVVACVCIHLACKWSNWEIPVSTDGKHWWEYVDATVTLELLDELTHEFLQILEKTPNRLKRIWNWRAC',
            'chains': ['BBB']}
        entity_dict['5'] = {'sequence': 'MEPVDPRLEPWKHPGSQPKTACTNCYCKKCCFHCQVCFITKALGISYGR',
                            'chains': ['DaD']}
        entity_dict['3'] = {'sequence': 'LFAEPYKVTSKEDKLSSRIQSMLGNYDEMKDFIG',
                            'chains': ['CCC']}
        entity_dict['1'] = {
            'sequence': 'VECPFCDEVSKYEKLAKIGGEVFKARHRKTGQKVALKKVLMENEKEGFPITALREIKILQLLKHENVVNLIEICRTKGSIYLVFDFCEHDLAGLLSNVLVKFTLSEIKRVMQMLLNGLYYIHRNKILHRDMKAANVLITRDGVLKLADFGLARAFSLAKNSQPNRYTNRVVTLWYRPPELLLGERDYGPPIDLWGAGCIMAEMWTRSPIMQGNTEQHQLALISQLCGSITPEVWPNVDNYELYEKLELVKGQKRKVKDRLKAYVRDPYALDLIDKLLVLDPAQRIDSDDALNHDFFWSDPMPSDLKGMLST',
            'chains': ['AAA']}
        entity_dict['6'] = {'sequence': 'GAUCUGAGCCUGGGAGCUCUC',
                            'chains': ['NNN']}
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
        mm = ExtractFromMmcif(mmcif_file=self.test_files.TEST_VALID_6fqf_FOUR_POLYMERS_WITH_SAME_SEQUENCE_MMCIF_FILE)
        entity_dict = dict()
        entity_dict['1'] = {
            'sequence': 'VHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFESFGDLSTPDAVMGNPKVKAHGKKVLGAFSDGLAHLDNLKGTFATLSELHCDKLHVDPENFRLLGNVLVCVLAHHFGKEFTPPVQAAYQKVVAGVANALAHKYH',
            'chains': ['AAA', 'BBB', 'CCC', 'DDD']}
        sequence_dict = mm.get_sequence_dict()
        self.assertFalse(sequence_dict == dict())
        for entity_id in entity_dict:
            chains = sequence_dict.get(entity_id, {}).get('chains', [])
            self.assertTrue(sequence_dict.get(entity_id, {}).get('sequence', '') == entity_dict[entity_id]['sequence'])
            self.assertTrue(sorted(chains) == sorted(entity_dict[entity_id]['chains']))

if __name__ == '__main__':
    unittest.main()
