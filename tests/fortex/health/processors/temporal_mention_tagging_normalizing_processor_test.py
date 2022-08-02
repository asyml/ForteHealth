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
Unit tests for TemporalMentionTaggingAndNormalizingProcessor
"""

import unittest

from forte.data.data_pack import DataPack
from forte.data.readers import StringReader
from forte.pipeline import Pipeline

from ftx.medical.clinical_ontology import MedicalArticle

from fortex.health.processors.temporal_mention_tagging_normalizing_processor import (
    TemporalMentionTaggingAndNormalizingProcessor,
)


class TestTemporalMentionTaggingAndNormalizingProcessor(unittest.TestCase):
    def setUp(self):
        self.nlp = Pipeline[DataPack](enforce_consistency=False)  # False
        self.nlp.set_reader(StringReader())
        config = {
            "entry_type": "ft.onto.base_ontology.Document",
            "attribute_name": "classification",
            "multi_class": True,
            "model_name": "satyaalmasian/temporal_tagger_BERT_tokenclassifier",
            "cuda_devices": -1,
        }

        self.nlp.add(
            TemporalMentionTaggingAndNormalizingProcessor(), config=config
        )  # , config=config
        self.nlp.initialize()

    def test_huggingface_TemporalMentionTaggingAndNormalizingProcessor(self):
        sentences = [
            "Due to lockdown restrictions, 2020 might go down as the worst economic year in over a decade.",
            # "Other related medical statements.",  # if this line is added the classification changed to T34.99
        ]
        document = "".join(sentences)
        print(document)
        pack = self.nlp.process(document)

        expected_mention = "2020"

        for idx, icd_coding_item in enumerate(pack.get(MedicalArticle)):
            # print(icd_coding_item.icd_code, idx)
            self.assertEqual(icd_coding_item.icd_code, expected_mention)
