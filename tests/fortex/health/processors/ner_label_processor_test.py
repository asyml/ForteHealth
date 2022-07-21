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
Unit tests for ICDCodingProcessor
"""

import unittest

from ddt import data, ddt
from forte.data.data_pack import DataPack
from forte.data.readers import StringReader
from forte.pipeline import Pipeline
from fortex.health.processors.ner_label_processor import NERLabelProcessor
from ftx.medical.clinical_ontology import Chemical, Disease


@ddt
class TestNERLabelProcessor(unittest.TestCase):

    @data(
        "He got cancer, and he needs oxygen."
    )
    def test_ner_label_processor(self, input_data):
        self.nlp = Pipeline[DataPack]()
        self.nlp.set_reader(StringReader())
        config = {
            "labels": ["disease", "chemical"]
        }

        self.nlp.add(NERLabelProcessor(), config=config)
        self.nlp.initialize()
        pack = self.nlp.process(input_data)

        exp_disease = ["cancer"]
        disease = []

        for idx, d in enumerate(pack.get(Disease)):
            disease.append(d.text)

        assert exp_disease == disease

        exp_chemical = ["oxygen"]
        chemical = []
        for idx, c in enumerate(pack.get(Chemical)):
            chemical.append(c.text)

        assert exp_chemical == chemical


if __name__ == "__main__":
    unittest.main()
