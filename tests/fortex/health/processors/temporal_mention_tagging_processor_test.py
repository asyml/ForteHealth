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

from ftx.medical.clinical_ontology import TemporalTag
# from fortex.health.processors.temporal_mention_tagging_processor import (
#     TemporalMentionTaggingProcessor,
# )

import sys
sys.path.append("/Users/nikhil.ranjan/Desktop/ForteHealth/fortex/health/processors")
from temporal_mention_tagging_processor import (
    TemporalMentionTaggingProcessor,
)


class TestTemporalMentionTaggingProcessor(unittest.TestCase):
    def setUp(self):
        self.nlp = Pipeline[DataPack](enforce_consistency=False)
        self.nlp.set_reader(StringReader())
        config = {
            "entry_type": "ft.onto.base_ontology.Document",
            "model_name": "satyaalmasian/temporal_tagger_BERT_tokenclassifier",
            "cuda_devices": -1,
        }

        self.nlp.add(
            TemporalMentionTaggingProcessor(), config=config
        ) 
        self.nlp.initialize()

    def test_huggingface_TemporalMentionTaggingProcessor(self):
        sentences = [
            "Due to lockdown restrictions, 2020 might go down as the worst economic year in over a decade.",
            "Is the the final year of the man behind the tomorrows killing at 2 pm in morning",
        ]
        document = "".join(sentences)
        pack = self.nlp.process(document)

        expected_mention = [
            "2020",
            "over a decade",
            "final year",
            "2 pm",
            "morning",
        ]

        for idx, tag in enumerate(pack.get(TemporalTag)):
            self.assertEqual(tag.entity, expected_mention[idx])

# a = TestTemporalMentionTaggingProcessor()
# a.setUp()
# a.test_huggingface_TemporalMentionTaggingProcessor()