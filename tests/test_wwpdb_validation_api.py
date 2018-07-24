import unittest
from tests.access_test_files import TestFiles
import tempfile
import os
import shutil

import adding_stats_to_mmcif.wwpdb_validation_api as wwpdb_validation_api


class TestValidationReportGeneration(unittest.TestCase):

    def setUp(self):
        self.test_files = TestFiles()

    def test_3zt9(self):
        test_dir = tempfile.mkdtemp()
        output_file = os.path.join(test_dir, 'output.pdf')
        self.test_files.one_sequence()
        worked, process_output_file = wwpdb_validation_api.run_validation_api(
            model_file_path=self.test_files.test_output_file,
            sf_file_path=self.test_files.structure_factor,
            output_file_name=output_file)
        self.assertTrue(worked)
        self.assertTrue(os.path.exists(process_output_file))
        self.assertTrue(output_file == process_output_file)
        shutil.rmtree(test_dir)


if __name__ == '__main__':
    unittest.main()
