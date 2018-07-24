import os


class TestFiles:

    def __init__(self):
        self.FILE_ROOT = os.path.dirname(os.path.realpath(__file__))
        self.path = os.path.dirname(os.path.join(self.FILE_ROOT, '..', '..'))
        self.test_data = os.path.join(self.path, 'test_data')
        self.TEST_AIMLESS_XML_FILE = os.path.join(self.test_data, "aimless_example.xml")
        self.TEST_AIMLESS_XML_FILE_NO_DATA = os.path.join(self.test_data, "aimless_example_no_data.xml")
        self.TEST_BAD_XML_FILE = os.path.join(self.test_data, "bad_example.xml")
        self.TEST_NON_AIMLESS_XML_FILE = os.path.join(self.test_data, "non_aimless_example.xml")
        self.TEST_INVALID_MMCIF_FILE = os.path.join(self.test_data, "invalid.cif")
        self.TEST_VALID_MMCIF_FILE = os.path.join(self.test_data, "valid.cif")
        self.TEST_INVALID_FASTA_ONE_SEQUENCE = os.path.join(self.test_data, "invalid.fasta")

        self.fasta = None
        self.cif = None
        self.sample_seq = None
        self.observed_seq = None
        self.sample_seq_to_obs_remapping = None
        self.exptl_data = None
        self.test_output_file = None
        self.structure_factor = None

    def one_sequence(self):
        self.fasta = os.path.join(self.test_data, "one_chain.fasta")
        self.cif = os.path.join(self.test_data, "pdb3zt9_refmac1.cif")
        self.sample_seq = {
            'pdb|3zt9|A': 'MEKLEVGIYTRAREGEIACGDACLVKRVEGVIFLAVGDGIGHGPEAARAAEIAIASMESSMNTGLVNIFQLCHRELRGTRGAVAALCRVDRRQGLWQAAIVGNIHVKILSAKGIITPLATPGILGYNYPHQLLIAKGSYQEGDLFLIHSDGIQEGAVPLALLANYRLTAEELVRLIGEKYGRRDDDVAVIVAR'}
        self.sample_seq_to_obs_remapping = {'1': 'pdb|3zt9|A'}
        self.observed_seq = dict()
        self.observed_seq['1'] = {
            'sequence': 'EKLEVGIYTRAREGEIACGDACLVKRVEGVIFLAVGDGIGHGPEAARAAEIAIASMESSMNTGLVNIFQLCHRELRGTRGAVAALCRVDRRQGLWQAAIVGNIHVKILSAKGIITPLATPGILGYNYPHQLLIAKGSYQEGDLFLIHSDGIQEGAVPLALLANYRLTAEELVRLIGEKYGRRDDDVAVIVAR',
            'chains': ['AAA']}
        self.exptl_data = {'_exptl.': {'entry_id': ['3ZT9'], 'method': ['X-RAY DIFFRACTION']}}
        self.test_output_file = os.path.join(self.test_data, "pdb3zt9_refmac1_output.cif")
        self.structure_factor = os.path.join(self.test_data, 'r3zt9sf.ent')

    def one_sequence_4hg7(self):
        self.fasta = os.path.join(self.test_data, "0021-03_4hg7.seq")
        self.cif = os.path.join(self.test_data, "deposition_refmac1.cif")
        self.sample_seq = {
            '4HG7:A|PDBID|CHAIN|SEQUENCE': 'GPLGSSQIPASEQETLVRPKPLLLKLLKSVGAQKDTYTMKEVLFYLGQYIMTKRLYDAAQQHIVYCSNDLLGDLFGVPSFSVKEHRKIYTMIYRNLV'}
        self.sample_seq_to_obs_remapping = {'1': '4HG7:A|PDBID|CHAIN|SEQUENCE'}
        self.observed_seq = dict()
        self.observed_seq['1'] = {
            'sequence': 'GPLGSSQIPASEQETLVRPKPLLLKLLKSVGAQKDTYTMKEVLFYLGQYIMTKRLYDAAQQHIVYCSNDLLGDLFGVPSFSVKEHRKIYTMIYRNLV',
            'chains': ['AAA']}

    def four_chains_one_polymer(self):
        self.fasta = os.path.join(self.test_data, "four_chains_one_polymer.fasta")
        self.cif = os.path.join(self.test_data, "pdb6fqf_refmac1.cif")
        self.sample_seq = {
            'pdb|6fqf|A B C D': 'VHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFESFGDLSTPDAVMGNPKVKAHGKKVLGAFSDGLAHLDNLKGTFATLSELHCDKLHVDPENFRLLGNVLVCVLAHHFGKEFTPPVQAAYQKVVAGVANALAHKYH'}
        self.sample_seq_to_obs_remapping = {'1': 'pdb|6fqf|A B C D'}
        self.observed_seq = dict()
        self.observed_seq['1'] = {
            'sequence': 'VHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFESFGDLSTPDAVMGNPKVKAHGKKVLGAFSDGLAHLDNLKGTFATLSELHCDKLHVDPENFRLLGNVLVCVLAHHFGKEFTPPVQAAYQKVVAGVANALAHKYH',
            'chains': ['AAA', 'BBB', 'CCC', 'DDD']}
        self.structure_factor = os.path.join(self.test_data, 'r6fqfsf.ent')

    def three_sequences(self):
        self.fasta = os.path.join(self.test_data, "three_chains.fasta")
        self.cif = os.path.join(self.test_data, 'pdb6db6_refmac1.cif')
        self.sample_seq = {'pdb|6db6|P': 'YNKRKRIHIGPGRAFYTTKNIIG',
                           'pdb|6db6|H': 'QVQLVQSGAEVKKPGASVKISCKASGYNFTTYAMHWVRQAPGQGLEWMGWINGGNGDTRYSQKFRGRVTISRDTSASTAYMELHSLTSEDTALFYCARESGDYYSEISGALDWGQGTLVTVSSASTKGPSVFPLAPSSKSTSGGTAALGCLVKDYFPEPVTVSWNSGALTSGVHTFPAVLQSSGLYSLSSVVTVPSSSLGTQTYICNVNHKPSNTKVDKRVEPKSCDKTH',
                           'pdb|6db6|L': 'SYELTQPPSVSVSPGQTARITCSGDVLPKKYAYWYQQKSGLAPVLVIYEDNRRPSGIPERFSGSSSGTMATLTISGAQVEDEGDYYCSSTDSSGDHYVFGTGTKVTVLGQPKANPSVTLFPPSSEELQANKATLVCLISDFYPGAVTVAWKADSSPVKAGVETTTPSKQSNNKYAASSYLSLTPEQWKSHRSYSCQVTHEGSTVEKTVAPTECS'}
        self.sample_seq_to_obs_remapping = {'1': 'pdb|6db6|H',
                                            '2': 'pdb|6db6|L',
                                            '3': 'pdb|6db6|P',
                                            }
        self.observed_seq = dict()
        self.observed_seq['1'] = {'sequence': 'QVQLVQSGAEVKKPGASVKISCKASGYNFTTYAMHWVRQAPGQGLEWMGWINGGNGDTRYSQKFRGRVTISRDTSASTAYMELHSLTSEDTALFYCARESGDYYSEISGALDWGQGTLVTVSSASTKGPSVFPLAPSSKSTSGGTAALGCLVKDYFPEPVTVSWNSGALTSGVHTFPAVLQSSGLYSLSSVVTVPSSSLGTQTYICNVNHKPSNTKVDKRVEPKSCDKTH',
                                  'chains': ['HHH']}
        self.observed_seq['3'] = {
            'sequence': 'YNKRKRIHIGPGRAFYTTKNIIG',
            'chains': ['PPP']}
        self.observed_seq['2'] = {
            'sequence': 'SYELTQPPSVSVSPGQTARITCSGDVLPKKYAYWYQQKSGLAPVLVIYEDNRRPSGIPERFSGSSSGTMATLTISGAQVEDEGDYYCSSTDSSGDHYVFGTGTKVTVLGQPKANPSVTLFPPSSEELQANKATLVCLISDFYPGAVTVAWKADSSPVKAGVETTTPSKQSNNKYAASSYLSLTPEQWKSHRSYSCQVTHEGSTVEKTVAPTECS',
            'chains': ['LLL']}
        self.structure_factor = os.path.join(self.test_data, 'r6bd6sf.ent')

    def five_sequences(self):
        self.fasta = os.path.join(self.test_data, "five_chains.fasta")
        self.cif = os.path.join(self.test_data, "5l1z_refmac1.cif")
        self.sample_seq = {
            'pdb|5l1z|B': 'MEGERKNNNKRWYFTREQLENSPSRRFGVDPDKELSYRQQAANLLQDMGQRLNVSQLTINTAIVYMHRFYMIQSFTQFPGNSVAPAALFLAAKVEEQPKKLEHVIKVAHTCLHPQESLPDTRSEAYLQQVQDLVILESIILQTLGFELTIDHPHTHVVKCTQLVRASKDLAQTSYFMATNSLHLTTFSLQYTPPVVACVCIHLACKWSNWEIPVSTDGKHWWEYVDATVTLELLDELTHEFLQILEKTPNRLKRIWNWRACEAA',
            'pdb|5l1z|D': 'XMEPVDPRLEPWKHPGSQPKTACTNCYCKKCCFHCQVCFITKALGISYGRKKRRQRRR',
            'pdb|5l1z|C': 'SPLFAEPYKVTSKEDKLSSRIQSMLGNYDEMKDFIG',
            'pdb|5l1z|A': 'MAKQYDSVECPFCDEVSKYEKLAKIGQGTFGEVFKARHRKTGQKVALKKVLMENEKEGFPITALREIKILQLLKHENVVNLIEICRTKASPYNRCKGSIYLVFDFCEHDLAGLLSNVLVKFTLSEIKRVMQMLLNGLYYIHRNKILHRDMKAANVLITRDGVLKLADFGLARAFSLAKNSQPNRYTNRVVTLWYRPPELLLGERDYGPPIDLWGAGCIMAEMWTRSPIMQGNTEQHQLALISQLCGSITPEVWPNVDNYELYEKLELVKGQKRKVKDRLKAYVRDPYALDLIDKLLVLDPAQRIDSDDALNHDFFWSDPMPSDLKGMLST',
            'pdb|5l1z|N': 'AGAUCUGAGCCUGGGAGCUCUCU'}

        self.sample_seq_to_obs_remapping = {'1': 'pdb|5l1z|A',
                                            '2': 'pdb|5l1z|B',
                                            '3': 'pdb|5l1z|C',
                                            '5': 'pdb|5l1z|D',
                                            '6': 'pdb|5l1z|N'}
        self.observed_seq = dict()
        self.observed_seq['2'] = {
            'sequence': 'NNNKRWYFTREQLENSPSRRFGVDPDKELSYRQQAANLLQDMGQRLNVSQLTINTAIVYMHRFYMIQSFTQFPGNSVAPAALFLAAKVEEQPKKLEHVIKVAHTCLHPQESLPDTRSEAYLQQVQDLVILESIILQTLGFELTIDHPHTHVVKCTQLVRASKDLAQTSYFMATNSLHLTTFSLQYTPPVVACVCIHLACKWSNWEIPVSTDGKHWWEYVDATVTLELLDELTHEFLQILEKTPNRLKRIWNWRAC',
            'chains': ['BBB']}
        self.observed_seq['5'] = {'sequence': 'MEPVDPRLEPWKHPGSQPKTACTNCYCKKCCFHCQVCFITKALGISYGR',
                                  'chains': ['DaD']}
        self.observed_seq['3'] = {'sequence': 'LFAEPYKVTSKEDKLSSRIQSMLGNYDEMKDFIG',
                                  'chains': ['CCC']}
        self.observed_seq['1'] = {
            'sequence': 'VECPFCDEVSKYEKLAKIGGEVFKARHRKTGQKVALKKVLMENEKEGFPITALREIKILQLLKHENVVNLIEICRTKGSIYLVFDFCEHDLAGLLSNVLVKFTLSEIKRVMQMLLNGLYYIHRNKILHRDMKAANVLITRDGVLKLADFGLARAFSLAKNSQPNRYTNRVVTLWYRPPELLLGERDYGPPIDLWGAGCIMAEMWTRSPIMQGNTEQHQLALISQLCGSITPEVWPNVDNYELYEKLELVKGQKRKVKDRLKAYVRDPYALDLIDKLLVLDPAQRIDSDDALNHDFFWSDPMPSDLKGMLST',
            'chains': ['AAA']}
        self.observed_seq['6'] = {'sequence': 'GAUCUGAGCCUGGGAGCUCUC',
                                  'chains': ['NNN']}
        self.structure_factor = os.path.join(self.test_data, 'r5l1zsf.ent')
