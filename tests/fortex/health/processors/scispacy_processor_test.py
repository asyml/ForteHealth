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
Unit tests for ScispaCyProcessor
"""

import unittest

from forte.data.data_pack import DataPack
from forte.data.readers import StringReader
from forte.pipeline import Pipeline

from ftx.medical.clinical_ontology import Hyponym, Abbreviation

from fortex.health.processors.scispacy_processor import (
    ScispaCyProcessor,
)


class TestScispaCyAbvProcessor(unittest.TestCase):
    def setUp(self):
        self.nlp = Pipeline[DataPack](enforce_consistency=True)
        self.nlp.set_reader(StringReader())
        config = {
            "entry_type": "ft.onto.base_ontology.Document",
            "model_name": "en_core_sci_sm",
            "pipe_name": "abbreviation_detector",
        }
        self.nlp.add(ScispaCyProcessor(), config=config)
        self.nlp.initialize()

    def test_ScispaCy_Abv_processor(self):
        sentences = [
            "Spinal and bulbar muscular atrophy (SBMA) is an \
            inherited motor neuron disease caused by the expansion \
            of a polyglutamine tract within the androgen receptor (AR). \
            SBMA can be caused by this easily."
        ]
        document = "".join(sentences)
        pack = self.nlp.process(document)

        expected_result = [
            ("SBMA", "Spinal and bulbar muscular atrophy"),
            ("AR", "androgen receptor"),
            ("SBMA", "Spinal and bulbar muscular atrophy"),
        ]

        for idx, abv_item in enumerate(pack.get(Abbreviation)):
            pipeline_output = (abv_item.text, abv_item.long_form.text)
            self.assertEqual(pipeline_output, expected_result[idx])


class TestScispaCyHyponymProcessor(unittest.TestCase):
    def setUp(self):

        self.nlp = Pipeline[DataPack](enforce_consistency=True)
        self.nlp.set_reader(StringReader())
        config = {
            "entry_type": "ft.onto.base_ontology.Document",
            "model_name": "en_core_sci_sm",
            "pipe_name": "hyponym_detector",
        }
        self.nlp.add(ScispaCyProcessor(), config=config)
        self.nlp.initialize()

    def test_ScispaCy_Hypomym_processor(self):

        sentences = [
            "Keystone plant species such as fig trees are good for the soil."
        ]
        document = "".join(sentences)
        pack = self.nlp.process(document)
        expected_value = {
            "hyponym_link": "such_as",
            "general": "Keystone plant species",
            "specific": "fig trees",
        }

        for idx, detected in enumerate(pack.get(Hyponym)):
            self.assertEqual(
                detected.hyponym_link, expected_value["hyponym_link"]
            )
            self.assertEqual(detected.general, expected_value["general"])
            self.assertEqual(detected.specific, expected_value["specific"])

if __name__ == "__main__":
    unittest.main()