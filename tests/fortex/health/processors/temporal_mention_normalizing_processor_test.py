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

from ftx.medical.clinical_ontology import NormalizedTemporalForm
from fortex.health.processors.temporal_mention_normalizing_processor import (
    TemporalMentionNormalizingProcessor,
)


class TestTemporalMentionNormalizingProcessor(unittest.TestCase):
    def setUp(self):
        self.nlp = Pipeline[DataPack](enforce_consistency=True)
        self.nlp.set_reader(StringReader())
        config = {
            "entry_type": "ft.onto.base_ontology.Document",
            "model_name": "en_core_web_sm",
            "pipe_name": "timexy",
        }
        self.nlp.add(TemporalMentionNormalizingProcessor(), config=config)
        self.nlp.initialize()

    def test_TemporalMentionNormalizingProcessor(self):
        sentences = ["10.10.2010", "10 days ago", "5 years later"]

        expected_normalization = [
            "2010-10-10T00:00:00",
            "P10D",
            "P5Y",
        ]
        pred_normalization = []

        for pack in self.nlp.process_dataset(sentences):
            for idx, normalized_item in enumerate(
                pack.get(NormalizedTemporalForm)
            ):
                pred_normalization.append(normalized_item.value)

        for exp, pred in zip(expected_normalization, pred_normalization):
            self.assertEqual(exp, pred)
