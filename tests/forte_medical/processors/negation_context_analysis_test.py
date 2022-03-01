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
Unit tests for NegationContextAnalyzer
"""

import unittest
from ddt import data, ddt

from forte.common import ProcessExecutionException
from forte.data.data_pack import DataPack
from forte.data.readers import StringReader
from forte.pipeline import Pipeline
from ft.onto.base_ontology import Sentence, EntityMention
from fortex.spacy import SpacyProcessor
from forte_medical.processors.negation_context_analyzer import NegationContextAnalyzer
from ftx.medical.clinical_ontology import NegationContext


@ddt
class TestNegationContextAnalyzer(unittest.TestCase):
    @data(
        "Abdominal CT showed no lesions of "
        "T10 and sacrum most likely secondary to osteoporosis. These can "
        "be followed by repeat imaging as an outpatient."
    )
    def test_pre_negation_detection(self, input_data):
        self.pl = (
            Pipeline[DataPack]()
            .set_reader(StringReader())
            .add(
                SpacyProcessor(),
                config={
                    "processors": ["sentence", "tokenize", "ner"],
                    "lang": "en_ner_bionlp13cg_md",
                })
            .add(
                NegationContextAnalyzer(),
                config={
                    "negation_rules_path": "../../../examples/mimic_iii/negex_triggers.txt",
                    "pre_negation_rules": [],
                    "post_negation_rules": [],
                    }
            )
            .initialize()
        )

        for pack in self.pl.process_dataset(input_data):
            for sentence in pack.get(Sentence):
                negationContexts = [(negations.text, negations.polarity) 
                        for negations in pack.get(NegationContext, sentence)]
                
                check = [('lesions', True), ('T10', True), ('sacrum', True)]

                assert negationContexts == check
                break

    @data(
        "Abdominal CT shows lesions are absent "
        "most likely secondary to osteoporosis. These can "
        "be followed by repeat imaging as an outpatient."
    )
    def test_post_negation_detection(self, input_data):
        self.pl = (
            Pipeline[DataPack]()
            .set_reader(StringReader())
            .add(
                SpacyProcessor(),
                config={
                    "processors": ["sentence", "tokenize", "ner"],
                    "lang": "en_ner_bionlp13cg_md",
                })
            .add(
                NegationContextAnalyzer(),
                config={
                    "negation_rules_path": "../../../examples/mimic_iii/negex_triggers.txt",
                    "pre_negation_rules": [],
                    "post_negation_rules": [],
                    }
            )
            .initialize()
        )

        for pack in self.pl.process_dataset(input_data):
            for sentence in pack.get(Sentence):
                negationContexts = [(negations.text, negations.polarity) 
                        for negations in pack.get(NegationContext, sentence)]
                
                check = [('lesions', True)]

                assert negationContexts == check
                break
    
    @data(
        "Abdominal CT shows lesions exist but "
        "no sacrum most likely secondary to osteoporosis. These can "
        "be followed by repeat imaging as an outpatient."
    )
    def test_negation_with_conj_detection(self, input_data):
        self.pl = (
            Pipeline[DataPack]()
            .set_reader(StringReader())
            .add(
                SpacyProcessor(),
                config={
                    "processors": ["sentence", "tokenize", "ner"],
                    "lang": "en_ner_bionlp13cg_md",
                })
            .add(
                NegationContextAnalyzer(),
                config={
                    "negation_rules_path": "../../../examples/mimic_iii/negex_triggers.txt",
                    "pre_negation_rules": [],
                    "post_negation_rules": [],
                    }
            )
            .initialize()
        )

        for pack in self.pl.process_dataset(input_data):
            for sentence in pack.get(Sentence):
                e = [ent.text for ent in pack.get(EntityMention, sentence)]
                print (e)
                negationContexts = [(negations.text, negations.polarity) 
                        for negations in pack.get(NegationContext, sentence)]
                
                check = [('lesions', False), ('sacrum', True)]

                assert negationContexts == check
                break
    
    @data(
        "ADDENDUM:"
        "ABDOMINAL CT:  Abdominal CT shows lesions but "
        "no sacrum most likely secondary to osteoporosis. These can "
        "be followed by repeat imaging as an outpatient."
    )
    def test_processing_error(self, input_data):
        self.pl = (
            Pipeline[DataPack]()
            .set_reader(StringReader())
            .add(
                SpacyProcessor(),
                config={
                    "processors": ["sentence", "tokenize", "ner"],
                    "lang": "en_ner_bionlp13cg_md",
                })
            .add(
                NegationContextAnalyzer(),
                config={
                    "negation_rules_path": "",
                    }
            ))

        with self.assertRaises(ProcessExecutionException) as context:
            self.pl.initialize()
