# Copyright 2021 The Forte Authors. All Rights Reserved.
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
Negation Context Analyser
"""
import re
from typing import Dict, Set

from ft.onto.base_ontology import Sentence
from forte.common import Resources
from forte.common.configuration import Config
from forte.data.data_pack import DataPack
from forte.processors.base import PackProcessor

from ftx.medical.clinical_ontology import NegationContext
from ftx.onto.clinical import MedicalEntityMention

__all__ = [
    "NegationContextAnalyzer",
]


class NegationContextAnalyzer(PackProcessor):
    r"""Implementation of NegationContextAnalyzer has been adapted from the
    NegEx algorithm, originally published by ....
    Paper link
    """

    def __init__(self):
        super().__init__()
        self.__rules = None

    def __sort_rules__ (self, rule_list: list[str]) -> list:
        r"""Return sorted list of rules.

        Rules should be in a tab-delimited format: 'rule_phrase\t\t[Tag]'
        Sorts list of rules descending based on length of the rule,
        splits each rule into components, converts pattern to regular expression,
        and appends it to the end of the rule.

        Types of Tags:
        [PREN] - Pre Negation rule
        [POST] - Post Negation rule
        [CONJ] - Conjunction phrase
        """

        rule_list.sort(key = len, reverse = True)
        sorted_list = []

        for rule in rule_list:
            rule_tokens = rule.strip().split('\t')
            rule_phrase_tokens = rule_tokens[0].split()
            rule_phrase = r'\s+'.join(rule_phrase_tokens)
            pattern = r'\b(' + rule_phrase + r')\b'
            rule_tokens.append(re.compile(pattern, re.IGNORECASE))
            sorted_list.append(rule_tokens)

        return sorted_list

    def set_up(self, configs: Config):
        if len(configs.negatin_rules_path) > 0:
            with open(configs.negation_rules_path, 'r', encoding='utf8') as rules_file:
                self.__rules = self.__sort_rules__(rules_file.readlines())
        else:
            raise ValueError("Please provide a file path for the negation rules"
                            + "to be used by the processor.")

    def initialize(self, resources: Resources, configs: Config):
        super().initialize(resources, configs)
        self.set_up(configs)

    def _process(self, input_pack: DataPack):
        r'''Exchanges the [PHRASE] ... [PHRASE] tags for [NEGATED] ... [NEGATED]
        based on PREN, POST rules.
        Because PRENEGATION [PREN} is checked first, it takes precedence over
        POSTNEGATION [POST].
        '''

        for sentence in input_pack.get(Sentence):
            filler = '_'

            for rule in self.__rules:
                reformat_rule = re.sub(r'\s+', filler, rule[0].strip())
                tagged_sentence = rule[3].sub (' ' + rule[2].strip()
                                                    + reformat_rule
                                                    + rule[2].strip() + ' ',
                                                sentence)

            for medical_entity in input_pack.get(MedicalEntityMention, sentence):
                for phrase in medical_entity.umls_entities:
                    # Precede all .,?+(){^* with a '\'
                    phrase = re.sub(r'([.^$*+?{\\|()[\]])', r'\\\1', phrase)
                    split_phrase = phrase.split()
                    joiner = r'\W+'
                    # To check for consecutive entities
                    joined_pattern = r'\b' + joiner.join(split_phrase) +  r'\b'
                    reP = re.compile(joined_pattern, re.IGNORECASE)
                    m = reP.search(tagged_sentence)
                    if m:
                        print (m.span())
                        tagged_sentence = tagged_sentence.replace(m.group(0), '[PHRASE]'
                                            + re.sub(r'\s+', filler, m.group(0).strip())
                                            + '[PHRASE]')

            overlap_flag = 0
            pre_negation_flag = 0
            post_negation_flag = 0

            sentence_tokens = tagged_sentence.split()
            #check for [PREN]
            for i, _ in enumerate(sentence_tokens):
                if sentence_tokens[i][:6] == '[PREN]':
                    pre_negation_flag = 1
                    overlap_flag = 0

                if sentence_tokens[i][:6] in ['[CONJ]', '[POST]']:
                    overlap_flag = 1

                if pre_negation_flag == 1 and overlap_flag == 0:
                    sentence_tokens[i] = sentence_tokens[i].replace('[PHRASE]', '[NEGATED]')

            sentence_tokens.reverse()
            # Check for [POST]
            for i, _ in enumerate(sentence_tokens):
                if sentence_tokens[i][:6] == '[POST]':
                    post_negation_flag = 1
                    overlap_flag = 0

                if sentence_tokens[i][:6] in ['[CONJ]', '[PREN]']:
                    overlap_flag = 1

                if post_negation_flag == 1 and overlap_flag == 0:
                    sentence_tokens[i] = sentence_tokens[i].replace('[PHRASE]', '[NEGATED]')

            sentence_tokens.reverse()
            tagged_sentence = ' '.join(sentence_tokens)

            r = re.compile(r'(\[NEGATED\]\w*\[NEGATED\])')
            neg_matches = r.findall(tagged_sentence)
            # print (neg_matches)
            r = re.compile(r'(\[PHRASE\]\w*\[PHRASE\])')
            pos_matches = r.findall(tagged_sentence)
            # print (pos_matches)

            tagged_sentence = re.sub(r'(\[\w*\])', '', tagged_sentence)

            for match in pos_matches:
                substring = re.sub(r'(\[\w*\])', '', match)
                pattern = r'\b' + substring + r'\b'
                result = re.search(pattern, tagged_sentence)
                print ("pos", result.span())
                negation_context = NegationContext(input_pack, result.span()[0], result.span()[1])
                negation_context.polarity = False

            for match in neg_matches:
                substring = re.sub(r'(\[\w*\])', '', match)
                pattern = r'\b' + substring + r'\b'
                result = re.search(pattern, tagged_sentence)
                print ("neg", result.span())
                negation_context = NegationContext(input_pack, result.span()[0], result.span()[1])
                negation_context.polarity = True

            tagged_sentence = tagged_sentence.replace(filler, ' ')

    @classmethod
    def default_configs(cls):
        r"""This defines a basic config structure for `QuestionAnsweringSingle`.

        Following are the keys for this dictionary:
            - `pre_negation_rules`: defines which entry type in the input pack to make
              prediction on. The default makes prediction on each `Document`
              in the input pack.
            - `post_negation_rules`: language model, default is
              `"ktrapeznikov/biobert_v1.1_pubmed_squad_v2"`.
              The wrapper supports Hugging Face models with pipeline tag of
              `question-answering`.
            - `negation_rules_path`: One question to retrieve answer from the input pack
              context.

        Returns: A dictionary with the default config for this processor.
        """
        return {
            "pre_negation_rules": [],
            "post_negation_rules": [],
            "negation_rules_path": "",
        }

    def expected_types_and_attributes(self):
        r"""Method to add user specified expected type which
        would be checked before running the processor if
        the pipeline is initialized with
        `enforce_consistency=True` or
        :meth:`~forte.pipeline.Pipeline.enforce_consistency` was enabled for
        the pipeline.
        """
        return {
            "ft.onto.base_ontology.EntityMention" : {"ner_type"},
        }

    def record(self, record_meta: Dict[str, Set[str]]):
        r"""Method to add output type record of `NegationContext` which
        is `"ftx.onto.clinical.NegationContext"` with attribute `polarity`
        to :attr:`forte.data.data_pack.Meta.record`.

        Args:
            record_meta: the field in the datapack for type record that need to
                fill in for consistency checking.
        """
        record_meta["ftx.onto.clinical.NegationContext"] = {"polarity"}
