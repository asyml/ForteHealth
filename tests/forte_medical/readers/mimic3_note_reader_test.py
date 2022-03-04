# Copyright 2022 The Forte Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Unit tests for Mimic3 Notes Reader
"""
import os
import tempfile
import unittest
from ddt import ddt, data

from forte.pipeline import Pipeline
from forte.data.data_pack import DataPack
from forte_medical.readers.mimic3_note_reader import Mimic3DischargeNoteReader


@ddt
class Mimic3ReaderPipelineTest(unittest.TestCase):
    def setUp(self):
        test_dir = tempfile.mkdtemp()
        self.orig_text = \
        '''
        ROW_ID","SUBJECT_ID","HADM_ID","CHARTDATE","CHARTTIME","STORETIME","CATEGORY","DESCRIPTION","CGID","ISERROR","TEXT"
        174,22532,167853,2151-08-04,,,"Discharge summary","Report",,,"Admission Date:  [**2151-7-16**]       Discharge Date:  [**2151-8-4**]

        Service:
        ADDENDUM:

        RADIOLOGIC STUDIES:  Radiologic studies also included a chest
        CT, which confirmed cavitary lesions in the left lung apex
        consistent with infectious process/tuberculosis.  This also
        moderate-sized left pleural effusion.'''

        file_path = os.path.join(test_dir, "test.csv")
        self.file_path = file_path
        with open(file_path, "w") as f:
            f.write(self.orig_text)

        self.reader = Mimic3DischargeNoteReader()
        self.pl = Pipeline[DataPack]()
        self.pl.set_reader(self.reader)
        self.pl.initialize()

    def test_reader(self):
        for pack in self.pl.process_dataset(self.file_path):
            self.assertEqual(self.orig_text, pack.text)

if __name__ == "__main__":
    unittest.main()
