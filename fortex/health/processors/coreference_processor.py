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
Coreference Processor
"""
import os
import re
from typing import Dict, List, Set
import importlib

from forte.common import Resources, ProcessExecutionException
from forte.common.configuration import Config
from forte.data.data_pack import DataPack
from forte.processors.base import PackProcessor

from ft.onto.base_ontology import CoreferenceGroup, Token
from ftx.medical.clinical_ontology import MedicalEntityMention, MedicalArticle

__all__ = [
    "CoreferenceProcessor",
]


class CoreferenceProcessor(PackProcessor):
    r"""
    TODO: Add docstring
    """

    def __init__(self):
        super().__init__()
        # TODO
        self.coref = None  # TODO: add type
        self.spacy_nlp = None  # TODO: find an elegant way to set this.

    def set_up(self, configs: Config):
        import neuralcoref

        self.spacy_nlp = self.resources.get("spacy_processor").nlp
        if self.spacy_nlp is None:
            raise ProcessExecutionException(
                "The SpaCy pipeline is not initialized, maybe you "
                "haven't called the initialization function."
            )
        kwargs = {}  # TODO
        neuralcoref.add_to_pipe(self.spacy_nlp)

    def initialize(self, resources: Resources, configs: Config):
        super().initialize(resources, configs)
        self.set_up(configs)

    def _process(self, input_pack: DataPack):
        r"""
        TODO: Add docstring
        """
        path_str, module_str = self.configs.entry_type.rsplit(".", 1)
        # By default, path_str would be ft.onto.base_ontology and module_str would be Document # TODO: check

        mod = importlib.import_module(path_str)
        entry = getattr(mod, module_str)
        for entry_specified in input_pack.get(entry_type=entry):
            result = self.spacy_nlp(entry_specified.text)
            tokens = [(token) for token in input_pack.get(Token, entry_specified)]

            article = MedicalArticle(
                pack=input_pack,
                begin=entry_specified.span.begin,
                end=entry_specified.span.end,
            )

            if not result._.has_coref:
                article.has_coref = False
                article.coref_groups = []
            else:
                article.has_coref = True
                article.coref_groups = []
                for cluster in result._.coref_clusters:

                    mentions = []
                    for mention in cluster.mentions:
                        mention = MedicalEntityMention(
                            input_pack,
                            tokens[mention.start].begin,
                            tokens[mention.end - 1].end,
                        )
                        mentions.append(mention)

                    group = CoreferenceGroup(input_pack)
                    group.add_members(mentions)

                    article.coref_groups.append(group)

    @classmethod
    def default_configs(cls):
        r"""
        TODO: Add docstring
        """
        return {
            # TODO: remove unnecessaries
            "entry_type": "ft.onto.base_ontology.Document",
        }

    def expected_types_and_attributes(self):
        r"""
        Method to add user specified expected type which would be checked
        before running the processor if the pipeline is initialized with
        `enforce_consistency=True` or
        :meth:`~forte.pipeline.Pipeline.enforce_consistency` was enabled for
        the pipeline.
        """
        return {
            # TODO
        }

    def record(self, record_meta: Dict[str, Set[str]]):
        r"""
        Method to add output type record of `CoreferenceProcessor` which
        is `"ftx.medical.clinical_ontology.MedicalArticle"` with attribute
        `coref_clusters`
        to :attr:`forte.data.data_pack.Meta.record`.

        Args:
            record_meta: the field in the datapack for type record that need to
                fill in for consistency checking.
        """  # TODO: check docstring
        # TODO
        record_meta["ftx.medical.clinical_ontology.MedicalArticle"] = {
            "coref_groups",
            "has_coref",
        }
