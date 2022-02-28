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
from typing import Dict, List, Set

from ft.onto.base_ontology import Sentence, EntityMention
from forte.common import Resources, ProcessExecutionException
from forte.common.configuration import Config
from forte.data.data_pack import DataPack
from forte.processors.base import PackProcessor

from ftx.medical.clinical_ontology import NegationContext

__all__ = [
    "NegationContextAnalyzer",
]


class NegationContextAnalyzer(PackProcessor):
    r"""
    Implementation of this NegationContextAnalyzer has been adapted from the
    NegEx algorithm, originally proposed in the paper 'A simple algorithm for identifying
    negated findings and diseases in discharge summaries', written by W.W. Chapman and others.
    A rendition of it that exists on github has been referred to as well.

    Paper link: https://pubmed.ncbi.nlm.nih.gov/12123149/
    """

    def __init__(self):
        super().__init__()
        self.__rules = None

    def __sort_rules(self, rule_list: List[str]) -> List:
        rule_list.sort(key=len, reverse=True)
        sorted_rules = []

        for rule in rule_list:
            rule_tokens = rule.strip().split('\t')
            rule_phrase_tokens = rule_tokens[0].split()
            rule_phrase = r'\s+'.join(rule_phrase_tokens)
            pattern = r'\b' + '(' + rule_phrase + ')' + r'\b'
            rule_tokens.append(pattern)
            sorted_rules.append(rule_tokens)

        return sorted_rules

    def set_up(self, configs: Config):
        if len(configs.negation_rules_path) > 0:
            with open(configs.negation_rules_path, 'r', encoding='utf8') as rules_file:
                self.__rules = self.__sort_rules(rules_file.readlines())
        else:
            raise ProcessExecutionException("Please provide a file path in config as "
                            + "config.negation_rules_pathfor the negation rules that will"
                            + "be used by the processor.")

    def initialize(self, resources: Resources, configs: Config):
        super().initialize(resources, configs)
        self.set_up(configs)

    def _process(self, input_pack: DataPack):
        r"""
        Negation Context analysis is done on the basis of tagging entities and detecting phrases.
        We use the negation rules' file to set all rule phrases which would convey a negative
        context depending on their positioning, before or after an entity.

        Rules should be in a tab-delimited format: 'rule_phrase\t\t[Tag]'
        Types of Tags:
        [PREN] - Pre Negation rule
        [POST] - Post Negation rule
        [CONJ] - Conjunction phrase

        Example rules from negation rules file:

        absence of      [PREN]
        does not exist  [POST]
        but             [CONJ]

        The first rule implies, if the phrase 'absence of' is present in the sentence before
        an entity, we annotate the entity as negation polarity=True. Similarly, if the phrase
        'does not exist' occurs in the sentence after an entity, it implies negative context.
        We also handle conjunctions, based off of rules from the rules' file.
        For example, given a sentence:

        "CT scan shows xyz but absence of lesions."
        Our implementation would set negation polarity for 'xyz' as False, but won't carry it to
        'lesions' because we detect 'but' as a conjunction in the sentence. Hence, we decide
        polarity for 'lesions' independently as True given the presence of 'absence' phrase before
        'lesions'.
        All rule phrases are tagged in the sentence as [PREN]..[PREN], [POST]..[POST] or
        [CONJ]..[CONJ], depending on how they are defined in the rules' file. All entity mentions
         are first annotated with the [ENTITY]..[ENTITY] tags.
        On negation detection, we replace those with [NEGATED]..[NEGATED].
        These tags are then used to define NegationContext annotations in the `input_pack` with
        corresponding polarity.
        """

        for sentence in input_pack.get(Sentence):
            filler = '_'
            tagged_sentence = sentence.text
            for rule in self.__rules:
                reformat_rule = re.sub(r'\s+', filler, rule[0].strip())
                tagged_sentence = re.sub(rule[3], rule[2].strip()
                                                    + reformat_rule
                                                    + rule[2].strip(),
                                                tagged_sentence)

            entities = [em.text for em in input_pack.get(EntityMention, sentence)]
            entities = set(entities)

            if len(entities) == 0:
                break

            for entity in entities:

                # Precede all ].,?+(){^* with a '\' so the special characters dont interfere
                # with the regex execution.
                entity = re.sub(r'([.^$*+?{\\|()[\]])', r'\\\1', entity)
                split_entity = entity.split()
                joiner = r'\W+'
                pattern = r'\b' + joiner.join(split_entity) + r'\b'
                entityPattern = re.compile(pattern, re.IGNORECASE)
                match = entityPattern.search(tagged_sentence)
                if match:
                    tagged_sentence = tagged_sentence.replace(match.group(0), '[ENTITY]'
                                        + re.sub(r'\s+', filler, match.group(0).strip())
                                        + '[ENTITY]')

            overlap_flag = 0
            pre_negation_flag = 0
            post_negation_flag = 0

            sentence_tokens = tagged_sentence.split()

            for i, _ in enumerate(sentence_tokens):
                if sentence_tokens[i][:6] == '[PREN]':
                    pre_negation_flag = 1
                    overlap_flag = 0

                if sentence_tokens[i][:6] in ['[CONJ]', '[POST]']:
                    overlap_flag = 1

                if pre_negation_flag == 1 and overlap_flag == 0:
                    sentence_tokens[i] = sentence_tokens[i].replace('[ENTITY]', '[NEGATED]')

            sentence_tokens.reverse()

            for i, _ in enumerate(sentence_tokens):
                if sentence_tokens[i][:6] == '[POST]':
                    post_negation_flag = 1
                    overlap_flag = 0

                if sentence_tokens[i][:6] in ['[CONJ]', '[PREN]']:
                    overlap_flag = 1

                if post_negation_flag == 1 and overlap_flag == 0:
                    sentence_tokens[i] = sentence_tokens[i].replace('[ENTITY]', '[NEGATED]')

            sentence_tokens.reverse()
            tagged_sentence = ' '.join(sentence_tokens)
            tagged_sentence = tagged_sentence.replace(filler, ' ')

            r = re.compile(r'(\[NEGATED\][\w|\s]*\[NEGATED\])')
            neg_matches = r.findall(tagged_sentence)

            r = re.compile(r'(\[ENTITY\][\w|\s]*\[ENTITY\])')
            pos_matches = r.findall(tagged_sentence)

            for match in pos_matches:
                substring = re.sub(r'(\[\w*\])', '', match)
                pattern = r'\b' + substring + r'\b'
                result = re.search(pattern, sentence.text)
                negation_context = NegationContext(input_pack,
                                        sentence.span.begin + result.span()[0],
                                        sentence.span.begin + result.span()[1])
                negation_context.polarity = False

            for match in neg_matches:
                substring = re.sub(r'(\[\w*\])', '', match)
                pattern = r'\b' + substring + r'\b'
                result = re.search(pattern, sentence.text)
                negation_context = NegationContext(input_pack,
                                        sentence.span.begin + result.span()[0],
                                        sentence.span.begin + result.span()[1])
                negation_context.polarity = True


    @classmethod
    def default_configs(cls):
        r"""
        This defines a basic config structure for `NegationContextAnalyzer`.

        Following are the keys for this dictionary:
            - `negation_rules_path`: provides the location of a rule phrases file, which would be
            used as triggers to detect negation context in sentences.

        Returns: A dictionary with the default config for this processor.
        """
        return {
            "negation_rules_path": "",
        }

    def expected_types_and_attributes(self):
        r"""
        Method to add user specified expected type which would be checked before running the
        processor if the pipeline is initialized with `enforce_consistency=True` or
        :meth:`~forte.pipeline.Pipeline.enforce_consistency` was enabled for the pipeline.
        """
        return {
            "ft.onto.base_ontology.EntityMention": {"ner_type"},
        }

    def record(self, record_meta: Dict[str, Set[str]]):
        r"""
        Method to add output type record of `NegationContext` which
        is `"ftx.onto.clinical.NegationContext"` with attribute `polarity`
        to :attr:`forte.data.data_pack.Meta.record`.

        Args:
            record_meta: the field in the datapack for type record that need to
                fill in for consistency checking.
        """
        record_meta["ftx.onto.clinical.NegationContext"] = {"polarity"}
