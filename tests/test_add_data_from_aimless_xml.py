import unittest
from adding_stats_to_mmcif.add_data_from_aimless_xml import aimless_software_row

class TestAddDataFromAimless(unittest.TestCase):

    def test_null_version(self):
        s = aimless_software_row()
        self.assertTrue(isinstance(s, dict))

if __name__ == '__main__':
    unittest.main()

