import unittest
from tests.access_test_files import TestFiles
from adding_stats_to_mmcif.add_sequence_to_mmcif import AddSequenceToMmcif
import tempfile
import os


class TestAddDataToMmcif(unittest.TestCase):

    def setUp(self):
        self.test_files = TestFiles()

    def test_get_data_from_3zt9_via_AddSequenceToMmcif(self):
        mm = AddSequenceToMmcif(input_mmcif=self.test_files.TEST_VALID_MMCIF_FILE,
                                output_mmcif='output.cif')
        entity_dict = dict()
        entity_dict['1'] = {
            'sequence': 'EKLEVGIYTRAREGEIACGDACLVKRVEGVIFLAVGDGIGHGPEAARAAEIAIASMESSMNTGLVNIFQLCHRELRGTRGAVAALCRVDRRQGLWQAAIVGNIHVKILSAKGIITPLATPGILGYNYPHQLLIAKGSYQEGDLFLIHSDGIQEGAVPLALLANYRLTAEELVRLIGEKYGRRDDDVAVIVAR',
            'chains': ['A']}
        sequence_dict = mm.process_mmcif()
        self.assertFalse(sequence_dict == dict())
        for entity_id in entity_dict:
            self.assertTrue(sequence_dict.get(entity_id, {}).get('sequence', '') == entity_dict[entity_id]['sequence'])
            self.assertTrue(sequence_dict.get(entity_id, {}).get('chains', []) == entity_dict[entity_id]['chains'])

    def test_get_data_from_6fqf_via_AddSequenceToMmcif(self):
        mm = AddSequenceToMmcif(input_mmcif=self.test_files.TEST_VALID_6fqf_FOUR_POLYMERS_WITH_SAME_SEQUENCE_MMCIF_FILE,
                                output_mmcif='output.cif')
        entity_dict = dict()
        entity_dict['1'] = {
            'sequence': 'VHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFESFGDLSTPDAVMGNPKVKAHGKKVLGAFSDGLAHLDNLKGTFATLSELHCDKLHVDPENFRLLGNVLVCVLAHHFGKEFTPPVQAAYQKVVAGVANALAHKYH',
            'chains': ['AAA', 'BBB', 'CCC', 'DDD']}
        sequence_dict = mm.process_mmcif()
        self.assertFalse(sequence_dict == dict())
        for entity_id in entity_dict:
            chains = sequence_dict.get(entity_id, {}).get('chains', [])
            self.assertTrue(sequence_dict.get(entity_id, {}).get('sequence', '') == entity_dict[entity_id]['sequence'])
            self.assertTrue(sorted(chains) == sorted(entity_dict[entity_id]['chains']))

    def test_get_data_from_5liz_via_AddSequenceToMmcif(self):
        mm = AddSequenceToMmcif(input_mmcif=self.test_files.TEST_VALID_5l1z_FIVE_POLYMERS_WITH_TPO_AND_RNA_MMCIF_FILE,
                                output_mmcif='output.cif')
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
        sequence_dict = mm.process_mmcif()
        self.assertFalse(sequence_dict == dict())
        for entity_id in entity_dict:
            chains = sequence_dict.get(entity_id, {}).get('chains', [])
            self.assertTrue(sequence_dict.get(entity_id, {}).get('sequence', '') == entity_dict[entity_id]['sequence'])
            self.assertTrue(sorted(chains) == sorted(entity_dict[entity_id]['chains']))

    def test_process_fasta_one_chain(self):

        expected_result = {
            'pdb|3zt9|A': 'MEKLEVGIYTRAREGEIACGDACLVKRVEGVIFLAVGDGIGHGPEAARAAEIAIASMESSMNTGLVNIFQLCHRELRGTRGAVAALCRVDRRQGLWQAAIVGNIHVKILSAKGIITPLATPGILGYNYPHQLLIAKGSYQEGDLFLIHSDGIQEGAVPLALLANYRLTAEELVRLIGEKYGRRDDDVAVIVAR'}
        mm = AddSequenceToMmcif(input_mmcif='input.cif', output_mmcif='output.cif',
                                fasta_file=self.test_files.TEST_VALID_FASTA_ONE_SEQUENCE)
        data = mm.process_input_sequences()
        self.assertTrue(len(data.keys()) == 1)
        for key in data:
            self.assertTrue(key in expected_result)
            self.assertTrue(data[key] == expected_result[key])

    def test_process_fasta_five_chains(self):
        expected_result = {
            'pdb|5l1z|B': 'MEGERKNNNKRWYFTREQLENSPSRRFGVDPDKELSYRQQAANLLQDMGQRLNVSQLTINTAIVYMHRFYMIQSFTQFPGNSVAPAALFLAAKVEEQPKKLEHVIKVAHTCLHPQESLPDTRSEAYLQQVQDLVILESIILQTLGFELTIDHPHTHVVKCTQLVRASKDLAQTSYFMATNSLHLTTFSLQYTPPVVACVCIHLACKWSNWEIPVSTDGKHWWEYVDATVTLELLDELTHEFLQILEKTPNRLKRIWNWRACEAA',
            'pdb|5l1z|D': 'XMEPVDPRLEPWKHPGSQPKTACTNCYCKKCCFHCQVCFITKALGISYGRKKRRQRRR',
            'pdb|5l1z|C': 'SPLFAEPYKVTSKEDKLSSRIQSMLGNYDEMKDFIG',
            'pdb|5l1z|A': 'MAKQYDSVECPFCDEVSKYEKLAKIGQGTFGEVFKARHRKTGQKVALKKVLMENEKEGFPITALREIKILQLLKHENVVNLIEICRTKASPYNRCKGSIYLVFDFCEHDLAGLLSNVLVKFTLSEIKRVMQMLLNGLYYIHRNKILHRDMKAANVLITRDGVLKLADFGLARAFSLAKNSQPNRYTNRVVTLWYRPPELLLGERDYGPPIDLWGAGCIMAEMWTRSPIMQGNTEQHQLALISQLCGSITPEVWPNVDNYELYEKLELVKGQKRKVKDRLKAYVRDPYALDLIDKLLVLDPAQRIDSDDALNHDFFWSDPMPSDLKGMLST',
            'pdb|5l1z|N': 'AGAUCUGAGCCUGGGAGCUCUCU'}

        mm = AddSequenceToMmcif(input_mmcif='input.cif', output_mmcif='output.cif',
                                fasta_file=self.test_files.TEST_VALID_FASTA_FIVE_SEQUENCES)
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
        mm = AddSequenceToMmcif(input_mmcif=self.test_files.TEST_VALID_MMCIF_FILE,
                                output_mmcif='output.cif',
                                fasta_file=self.test_files.TEST_VALID_FASTA_ONE_SEQUENCE)
        entity_dict = dict()
        entity_dict['1'] = {
            'sequence': 'EKLEVGIYTRAREGEIACGDACLVKRVEGVIFLAVGDGIGHGPEAARAAEIAIASMESSMNTGLVNIFQLCHRELRGTRGAVAALCRVDRRQGLWQAAIVGNIHVKILSAKGIITPLATPGILGYNYPHQLLIAKGSYQEGDLFLIHSDGIQEGAVPLALLANYRLTAEELVRLIGEKYGRRDDDVAVIVAR',
            'chains': ['A']}
        worked = mm.process_data()
        self.assertTrue(worked)

    def test_get_data_from_3zt9_via_AddSequenceToMmcif_get_best_match(self):
        expected_result = 'MEKLEVGIYTRAREGEIACGDACLVKRVEGVIFLAVGDGIGHGPEAARAAEIAIASMESSMNTGLVNIFQLCHRELRGTRGAVAALCRVDRRQGLWQAAIVGNIHVKILSAKGIITPLATPGILGYNYPHQLLIAKGSYQEGDLFLIHSDGIQEGAVPLALLANYRLTAEELVRLIGEKYGRRDDDVAVIVAR'
        entity_dict = dict()
        entity_dict['1'] = {
            'sequence': 'EKLEVGIYTRAREGEIACGDACLVKRVEGVIFLAVGDGIGHGPEAARAAEIAIASMESSMNTGLVNIFQLCHRELRGTRGAVAALCRVDRRQGLWQAAIVGNIHVKILSAKGIITPLATPGILGYNYPHQLLIAKGSYQEGDLFLIHSDGIQEGAVPLALLANYRLTAEELVRLIGEKYGRRDDDVAVIVAR',
            'chains': ['A']}
        mm = AddSequenceToMmcif(input_mmcif=self.test_files.TEST_VALID_MMCIF_FILE,
                                output_mmcif='output.cif',
                                fasta_file=self.test_files.TEST_VALID_FASTA_ONE_SEQUENCE)
        mm.process_input_sequences()
        best_seq, best_score = mm.get_best_match(mmcif_sequence=entity_dict['1']['sequence'])
        self.assertTrue(best_seq == expected_result)


if __name__ == '__main__':
    unittest.main()
