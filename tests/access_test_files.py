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
        self.TEST_VALID_FASTA_ONE_SEQUENCE = os.path.join(self.test_data, "one_chain.fasta")
        self.TEST_VALID_FASTA_THREE_SEQUENCES = os.path.join(self.test_data, "three_chain.fasta")
        self.TEST_INVALID_FASTA_ONE_SEQUENCE = os.path.join(self.test_data, "invalid.fasta")
