import unittest
from tests.access_test_files import TestFiles
import tempfile
import os
import shutil

from adding_stats_to_mmcif import run_process


class TestWholeProcess(unittest.TestCase):

    def setUp(self):
        self.test_files = TestFiles()

    def test_3zt9(self):
        test_dir = tempfile.mkdtemp()
        output_cif = os.path.join(test_dir, 'output.cif')
        self.test_files.one_sequence()
        worked = run_process(input_mmcif=self.test_files.cif, output_mmcif=output_cif,
                             fasta_file=self.test_files.fasta,
                             xml_file=self.test_files.TEST_AIMLESS_XML_FILE,
                             )
        self.assertTrue(worked)
        self.assertTrue(os.path.exists(output_cif))
        shutil.rmtree(test_dir)

    def test_5l1z(self):
        test_dir = tempfile.mkdtemp()
        output_cif = os.path.join(test_dir, 'output.cif')
        self.test_files.five_sequences()
        worked = run_process(input_mmcif=self.test_files.cif, output_mmcif=output_cif,
                             fasta_file=self.test_files.fasta,
                             xml_file=self.test_files.TEST_AIMLESS_XML_FILE,
                             )
        self.assertTrue(worked)
        self.assertTrue(os.path.exists(output_cif))
        shutil.rmtree(test_dir)


if __name__ == '__main__':
    unittest.main()
