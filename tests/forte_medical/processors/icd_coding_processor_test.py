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

from forte.data.data_pack import DataPack
from forte.data.readers import StringReader
from forte.pipeline import Pipeline

from ftx.medical.clinical_ontology import MedicalArticle

from forte.health.processors.icd_coding_processor import (
    ICDCodingProcessor,
)


class TestICDCodeProcessor(unittest.TestCase):
    def setUp(self):
        self.nlp = Pipeline[DataPack](enforce_consistency=True)  # False
        self.nlp.set_reader(StringReader())
        config = {
            "entry_type": "ft.onto.base_ontology.Document",
            "attribute_name": "classification",
            "multi_class": True,
            "model_name": "AkshatSurolia/ICD-10-Code-Prediction",
            "cuda_devices": -1,
        }

        self.nlp.add(ICDCodingProcessor(), config=config)  # , config=config
        self.nlp.initialize()

    def test_huggingface_ICDCode_processor(self):
        sentences = [
            "subarachnoid hemorrhage scalp laceration service: surgery major surgical or invasive.",
            # "Other related medical statements.",  # if this line is added the classification changed to T34.99
        ]
        document = "".join(sentences)
        print(document)
        pack = self.nlp.process(document)

        expected_code = "H59.11"

        for idx, icd_coding_item in enumerate(pack.get(MedicalArticle)):
            # print(icd_coding_item.icd_code, idx)
            self.assertEqual(icd_coding_item.icd_code, expected_code)
