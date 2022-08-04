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

from temporal_mention_tagging_normalizing_processor import (
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
            "Today is monday, but tomorrow might be 12th july.",
            "A century ago, I was supposed to be here 1 day before that time.",
            "Before the diagnosis, the patient was declared dead, five hours ago at 10:23.",
            "April 23, 2014: The patient did not have any postoperative bleeding so we’ll resume chemotherapy with a larger bolus on Friday even if there is slight nausea."
            # "Other related medical statements.",  # if this line is added the classification changed to T34.99
        ]
        document = " ".join(sentences)
        print(document)
        for sent in sentences:
            self.nlp.process(sent)
        
        #pack = self.nlp.process(document)

        expected_mention = "2020"

        for idx, icd_coding_item in enumerate(pack.get(MedicalArticle)):
            print(icd_coding_item.icd_code, idx)
            #self.assertEqual(icd_coding_item.icd_code, expected_mention)

test = TestTemporalMentionTaggingAndNormalizingProcessor()
test.setUp()
test.test_huggingface_TemporalMentionTaggingAndNormalizingProcessor()