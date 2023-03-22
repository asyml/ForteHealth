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
Unit tests for multiple processor which include TemporalMentionTaggingProcessor and TemporalMentionNormalizingProcessor
"""

import unittest

from forte.data.data_pack import DataPack
from forte.data.readers import StringReader
from forte.pipeline import Pipeline

from ftx.medical.clinical_ontology import TemporalTag
from ftx.medical.clinical_ontology import NormalizedTemporalForm

from fortex.health.processors.temporal_mention_tagging_processor import (
    TemporalMentionTaggingProcessor,
)
from fortex.health.processors.temporal_mention_normalizing_processor import (
    TemporalMentionNormalizingProcessor,
)


class TestTemporalMentionTaggingProcessor(unittest.TestCase):
    def setUp(self):
        self.nlp = Pipeline[DataPack](enforce_consistency=False)
        self.nlp.set_reader(StringReader())
        config_tagger = {
            "entry_type": "ft.onto.base_ontology.Document",
            "model_name": "satyaalmasian/temporal_tagger_BERT_tokenclassifier",
            "cuda_devices": -1,
        }

        self.nlp.add(TemporalMentionTaggingProcessor(), config=config_tagger)

        config_normalizer = {
            "entry_type": "ftx.medical.clinical_ontology.TemporalTag",
            "model_name": "en_core_web_sm",
            "pipe_name": "timexy",
        }
        self.nlp.add(
            TemporalMentionNormalizingProcessor(), config=config_normalizer
        )

        self.nlp.initialize()

    def test_huggingface_TemporalMentionTaggingProcessor(self):
        sentences = [
            "I received this result 10 days ago.",
            "Please come for checkup after 5 years",
        ]
        document = " ".join(sentences)
        pack = self.nlp.process(document)

        expected_entity = ["10 days ago", "5 years"]

        expected_normalization = [
            ("P10D", "DURATION"),
            ("P5Y", "DURATION"),
        ]

        for idx, tag in enumerate(pack.get(TemporalTag)):
            self.assertEqual(tag.entity, expected_entity[idx])

        for idx, normalized_item in enumerate(pack.get(NormalizedTemporalForm)):
            self.assertEqual(
                expected_normalization[idx],
                (normalized_item.value, normalized_item.type),
            )
