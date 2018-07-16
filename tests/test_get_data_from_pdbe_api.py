import unittest
from adding_stats_to_mmcif.get_data_from_pdbe_api import GetDataFromPdbeAPi, GetSpecificDataFromPdbeAPI

class TestAddDataFromAimless(unittest.TestCase):

    def test_null_entry(self):
        s = GetDataFromPdbeAPi(entry_id=None, end_point='compounds').return_data()
        self.assertEqual(s, dict())

    def test_null_server(self):
        s = GetDataFromPdbeAPi(entry_id='ATP', end_point='compounds', server_root=None).return_data()
        self.assertEqual(s, dict())

    def test_incorrect_server_within_api(self):
        s = GetDataFromPdbeAPi(entry_id='ATP', end_point='compounds', server_root='https://www.ebi.ac.uk/pdbe/apiWRONG/').return_data()
        self.assertEqual(s, dict())

    def test_incorrect_server_url(self):
        s = GetDataFromPdbeAPi(entry_id='ATP', end_point='compounds', server_root='https://www.ebiWRONG.ac.uk/pdbe/api/').return_data()
        self.assertEqual(s, dict())

    def test_null_end_point(self):
        s = GetDataFromPdbeAPi(entry_id='ATP', end_point=None).return_data()
        self.assertEqual(s, dict())

    def test_unknown_end_point(self):
        s = GetDataFromPdbeAPi(entry_id='ATP', end_point='cheese').return_data()
        self.assertEqual(s, dict())

    def test_unknown_entry_id(self):
        s = GetDataFromPdbeAPi(entry_id='XXXXXXXXXXX', end_point='compounds').return_data()
        self.assertEqual(s, dict())
    
    def test_known_entry_id(self):
        s = GetDataFromPdbeAPi(entry_id='ATP', end_point='compounds').return_data()
        self.assertNotEqual(s, dict())

    def test_known_lower_case_entry_id(self):
        s = GetDataFromPdbeAPi(entry_id='atp', end_point='compounds').return_data()
        self.assertEqual(s, dict())

    def test_get_one_letter_code_for_tpo(self):
        s = GetSpecificDataFromPdbeAPI().get_one_letter_code_for_compound(compound='TPO')
        self.assertEqual(s, 'T')

    def test_get_one_letter_code_for_tpo_lower(self):
        s = GetSpecificDataFromPdbeAPI().get_one_letter_code_for_compound(compound='tpo')
        self.assertEqual(s, 'T')

    def test_get_one_letter_code_for_ATP(self):
        s = GetSpecificDataFromPdbeAPI().get_one_letter_code_for_compound(compound='ATP')
        self.assertEqual(s, 'X')

    def test_get_one_letter_code_for_unknown_ligand(self):
        s = GetSpecificDataFromPdbeAPI().get_one_letter_code_for_compound(compound='XXXXXXXXXXX')
        self.assertEqual(s, 'X')

    def test_get_one_letter_code_for_None_ligand(self):
        s = GetSpecificDataFromPdbeAPI().get_one_letter_code_for_compound(compound=None)
        self.assertEqual(s, 'X')

if __name__ == '__main__':
    unittest.main()
