import unittest

from ddt import ddt, data

from forte_medical.readers.mimic3_note_reader import Mimic3DischargeNoteReader


@ddt
class TestMimic3DischargeNoteReader(unittest.TestCase):
    @data('xxx')
    def test_mimic3_discharge_note_reader(self, mimic3_path):
        # TODO: write test
        self.assertEqual(mimic3_path, 'xxx')


if __name__ == "__main__":
    unittest.main()
