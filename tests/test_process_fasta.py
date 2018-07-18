import unittest
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
        expected_result = {'pdb|3zt9|A':'MEKLEVGIYTRAREGEIACGDACLVKRVEGVIFLAVGDGIGHGPEAARAAEIAIASMESSMNTGLVNIFQLCHRELRGTRGAVAALCRVDRRQGLWQAAIVGNIHVKILSAKGIITPLATPGILGYNYPHQLLIAKGSYQEGDLFLIHSDGIQEGAVPLALLANYRLTAEELVRLIGEKYGRRDDDVAVIVAR'}
        pf = ProcessFasta(fasta_file=self.test_files.TEST_VALID_FASTA_ONE_SEQUENCE)
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
        expected_result = {'pdb|6db6|P': 'YNKRKRIHIGPGRAFYTTKNIIG',
                           'pdb|6db6|H': 'QVQLVQSGAEVKKPGASVKISCKASGYNFTTYAMHWVRQAPGQGLEWMGWINGGNGDTRYSQKFRGRVTISRDTSASTAYMELHSLTSEDTALFYCARESGDYYSEISGALDWGQGTLVTVSSASTKGPSVFPLAPSSKSTSGGTAALGCLVKDYFPEPVTVSWNSGALTSGVHTFPAVLQSSGLYSLSSVVTVPSSSLGTQTYICNVNHKPSNTKVDKRVEPKSCDKTH',
                           'pdb|6db6|L': 'SYELTQPPSVSVSPGQTARITCSGDVLPKKYAYWYQQKSGLAPVLVIYEDNRRPSGIPERFSGSSSGTMATLTISGAQVEDEGDYYCSSTDSSGDHYVFGTGTKVTVLGQPKANPSVTLFPPSSEELQANKATLVCLISDFYPGAVTVAWKADSSPVKAGVETTTPSKQSNNKYAASSYLSLTPEQWKSHRSYSCQVTHEGSTVEKTVAPTECS'}
        pf = ProcessFasta(fasta_file=self.test_files.TEST_VALID_FASTA_THREE_SEQUENCES)
        pf.process_fasta_file()
        data = pf.get_sequence_dict()
        self.assertTrue(len(data.keys()) == 3)
        for key in data:
            self.assertTrue(key in expected_result)
            self.assertTrue(data[key] == expected_result[key])

    def test_valid_file_five_sequences(self):
        expected_result = {'pdb|5l1z|B': 'MEGERKNNNKRWYFTREQLENSPSRRFGVDPDKELSYRQQAANLLQDMGQRLNVSQLTINTAIVYMHRFYMIQSFTQFPGNSVAPAALFLAAKVEEQPKKLEHVIKVAHTCLHPQESLPDTRSEAYLQQVQDLVILESIILQTLGFELTIDHPHTHVVKCTQLVRASKDLAQTSYFMATNSLHLTTFSLQYTPPVVACVCIHLACKWSNWEIPVSTDGKHWWEYVDATVTLELLDELTHEFLQILEKTPNRLKRIWNWRACEAA',
                           'pdb|5l1z|D': 'XMEPVDPRLEPWKHPGSQPKTACTNCYCKKCCFHCQVCFITKALGISYGRKKRRQRRR',
                           'pdb|5l1z|C': 'SPLFAEPYKVTSKEDKLSSRIQSMLGNYDEMKDFIG',
                           'pdb|5l1z|A': 'MAKQYDSVECPFCDEVSKYEKLAKIGQGTFGEVFKARHRKTGQKVALKKVLMENEKEGFPITALREIKILQLLKHENVVNLIEICRTKASPYNRCKGSIYLVFDFCEHDLAGLLSNVLVKFTLSEIKRVMQMLLNGLYYIHRNKILHRDMKAANVLITRDGVLKLADFGLARAFSLAKNSQPNRYTNRVVTLWYRPPELLLGERDYGPPIDLWGAGCIMAEMWTRSPIMQGNTEQHQLALISQLCGSITPEVWPNVDNYELYEKLELVKGQKRKVKDRLKAYVRDPYALDLIDKLLVLDPAQRIDSDDALNHDFFWSDPMPSDLKGMLST',
                           'pdb|5l1z|N': 'AGAUCUGAGCCUGGGAGCUCUCU'}
        pf = ProcessFasta(fasta_file=self.test_files.TEST_VALID_FASTA_FIVE_SEQUENCES)
        pf.process_fasta_file()
        data = pf.get_sequence_dict()
        self.assertTrue(len(data.keys()) == 5)
        for key in data:
            self.assertTrue(key in expected_result)
            self.assertTrue(data[key] == expected_result[key])


if __name__ == '__main__':
    unittest.main()
