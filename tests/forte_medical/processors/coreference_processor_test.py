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
Unit tests for CoreferenceProcessor
"""

import unittest
from ddt import data, ddt

from forte.data.data_pack import DataPack
from forte.data.readers import StringReader
from forte.pipeline import Pipeline

from ftx.medical.clinical_ontology import MedicalArticle
from ft.onto.base_ontology import (
    Token,
)

from fortex.spacy import SpacyProcessor
from fortex.health.processors.coreference_processor import (
    CoreferenceProcessor,
)

@ddt
class TestCoreferenceProcessor(unittest.TestCase):
    def setUp(self):
        self.pl = Pipeline[DataPack](enforce_consistency=True)
        self.pl.set_reader(StringReader())
        self.pl.add(
            SpacyProcessor(),
            {"processors": ["sentence", "tokenize"], "lang": "en_core_web_sm"},
        )
        self.pl.add(
            CoreferenceProcessor(),
            {
                "entry_type": "ft.onto.base_ontology.Document",
                "mention_type": "ftx.medical.clinical_ontology.MedicalEntityMention",
                "lang": "en_core_web_sm",
                "model": True,
                "greedyness": 0.5,
                "max_dist": 50,
                "max_dist_match": 500,
                "blacklist": True,
                "store_scores": True,
                "conv_dict": None,
            },
        )

        self.pl.initialize()

    @data("My sister has a dog. She loves him.")
    def test_daily_language(self, input_data):
        for pack in self.pl.process_dataset(input_data):
            for article in pack.get(MedicalArticle):
                has_coref = article.has_coref
                assert has_coref == True

                coref_groups = article.coref_groups
                output_list = []
                check_list = [["My sister", "She"], ["a dog", "him"]]
                for group in coref_groups:
                    members = [member for member in group.get_members()]
                    members = sorted(members, key=lambda x: x.begin)

                    mention_texts = [member.text for member in members]
                    output_list.append(mention_texts)
                assert output_list == check_list

    @data(
        """ADDENDUM:
RADIOLOGIC STUDIES: Radiologic studies also included a chest CT, which confirmed cavitary lesions in the left lung apex consistent with infectious process/tuberculosis.
This also moderate-sized left pleural effusion.
HEAD CT: Head CT showed no intracranial hemorrhage and no mass effect, but old infarction consistent with past medical history.
ABDOMINAL CT:  Abdominal CT showed no lesions of T10 and sacrum most likely secondary to steoporosis.
These can be followed by repeat imaging as an outpatient."""
    )
    def test_medical_notes(self, input_data):
        for pack in self.pl.process_dataset(input_data):
            for article in pack.get(MedicalArticle):
                has_coref = article.has_coref
                assert has_coref == True

                coref_groups = article.coref_groups
                output_list = []
                check_list = [["HEAD CT", "Head CT", "Abdominal CT"]]
                for group in coref_groups:
                    members = [member for member in group.get_members()]
                    members = sorted(members, key=lambda x: x.begin)

                    mention_texts = [member.text for member in members]
                    output_list.append(mention_texts)
                assert output_list == check_list
