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

import importlib
import unittest
from ddt import data, ddt, unpack

from forte.data.data_pack import DataPack
from forte.data.readers import StringReader
from forte.pipeline import Pipeline

from ft.onto.base_ontology import Document, CoreferenceGroup
from fortex.health.processors.coreference_processor import (
    CoreferenceProcessor,
)
from fortex.spacy import SpacyProcessor


@ddt
class TestCoreferenceProcessor(unittest.TestCase):
    # def setUp(self):
    #     self.pl = Pipeline[DataPack](enforce_consistency=True)
    #     self.pl.set_reader(StringReader())
    #     self.pl.add(
    #         CoreferenceProcessor(),
    #         {
    #             "entry_type": "ft.onto.base_ontology.Document",
    #             "mention_type": "ftx.medical.clinical_ontology.MedicalEntityMention",
    #             "lang": "en_core_web_sm",
    #             "model": "use_default_model",
    #             "cfg_inference": {
    #                 "greedyness": 0.5,
    #                 "max_dist": 50,
    #                 "max_dist_match": 500,
    #                 "blacklist": True,
    #                 "store_scores": True,
    #                 "conv_dict": None,
    #             },
    #         },
    #     )

    #     self.pl.initialize()

    @data(
        (
            "ADDENDUM:\n"
            "RADIOLOGIC STUDIES: Radiologic studies also included "
            "a chest CT, which confirmed cavitary lesions "
            "in the left lung apex consistent with infectious process/tuberculosis.\n"
            "This also moderate-sized left pleural effusion.\n"
            "HEAD CT: Head CT showed no intracranial hemorrhage and no mass effect, "
            "but old infarction consistent with past medical history.\n"
            "ABDOMINAL CT:  Abdominal CT showed no lesions of T10 and sacrum "
            "most likely secondary to steoporosis.\n"
            "These can be followed by repeat imaging as an outpatient.",
            [["HEAD CT", "Head CT", "Abdominal CT"]],
            "ft.onto.base_ontology.Document",
        ),
        (
            "My sister has a dog. She loves him.",
            [["My sister", "She"], ["a dog", "him"]],
            "ft.onto.base_ontology.Document",
        ),
        (
            "My sister loves her dog. My aunt also loves him.",
            [["My sister", "her"], ["My aunt", "him"]],
            "ft.onto.base_ontology.Sentence",
        ),
        (
            "My sister loves her dog. My aunt also loves him.",
            [["My sister", "her"], ["her dog", "him"]],
            "ft.onto.base_ontology.Document",
            # Document-level coref is different from sentence-level.
        ),
    )
    @unpack
    def test_medical_notes(self, input_data, check_list, entry_type):
        self.pl = Pipeline[DataPack](enforce_consistency=True)
        self.pl.set_reader(StringReader())
        self.pl.add(SpacyProcessor(), config={"lang": "en_core_web_sm"})
        self.pl.add(
            CoreferenceProcessor(),
            {
                "entry_type": entry_type,
                "mention_type": "ftx.medical.clinical_ontology.MedicalEntityMention",
                "lang": "en_core_web_sm",
                "model": "use_default_model",
                "cfg_inference": {
                    "greedyness": 0.5,
                    "max_dist": 50,
                    "max_dist_match": 500,
                    "blacklist": True,
                    "store_scores": True,
                    "conv_dict": None,
                },
            },
        )

        self.pl.initialize()

        def load_module(string):
            path_str, module_str = string.rsplit(".", 1)
            mod = importlib.import_module(path_str)
            return getattr(mod, module_str)

        entry_type = load_module(entry_type)

        for pack in self.pl.process_dataset(input_data):
            output_list = []

            for document in pack.get(entry_type):
                for group in document.get(CoreferenceGroup):
                    members = [member for member in group.get_members()]
                    members = sorted(members, key=lambda x: x.begin)

                    mention_texts = [member.text for member in members]
                    output_list.append(mention_texts)

            self.assertEqual(output_list, check_list, f"input: {document.text}")
