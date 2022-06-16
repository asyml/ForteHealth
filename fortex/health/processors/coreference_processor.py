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
from typing import Dict, Optional, Set
import importlib
from boto import config

from spacy.language import Language

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
    Implementation of this CoreferenceProcessor has been based on huggingface
    NeuralCoref. Note that official released NeuralCoref uses a dated spaCy
    version (2.1), which can cause segmentation fault with the spaCy we use (2.3).
    Please install NeuralCoref by building from source:

    https://github.com/huggingface/neuralcoref
    """

    def __init__(self):
        super().__init__()
        self.spacy_nlp: Optional[Language] = None  # TODO: a more elegant way

    def set_up(self, configs: Config):
        import neuralcoref

        self.spacy_nlp = self.resources.get("spacy_processor").nlp
        if self.spacy_nlp is None:
            raise ProcessExecutionException(
                "The SpaCy pipeline is not initialized, maybe you "
                "haven't called the initialization function."
            )

        model = configs.model
        cfg_inference = {
            "greedyness": configs.greedyness,
            "max_dist": configs.max_dist,
            "max_dist_match": configs.max_dist_match,
            "blacklist": configs.blacklist,
            "store_scores": configs.store_scores,
            "conv_dict": configs.conv_dict,
        }
        neuralcoref.add_to_pipe(
            self.spacy_nlp, model=model, cfg_inference=cfg_inference
        )

    def initialize(self, resources: Resources, configs: Config):
        super().initialize(resources, configs)
        self.set_up(configs)

    def _process(self, input_pack: DataPack):
        r"""
        TODO: Add docstring
        """
        path_str, module_str = self.configs.entry_type.rsplit(".", 1)
        # By default, path_str would be ft.onto.base_ontology
        # and module_str would be Document # TODO: check

        mod = importlib.import_module(path_str)
        entry_type = getattr(mod, module_str)
        for entry_specified in input_pack.get(entry_type=entry_type):
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

    # @classmethod
    # def default_configs(cls):
    #     r"""
    #     This defines a basic config structure for `CoreferenceProcessor`.

    #     Following are the keys for this dictionary:
    #      - `entry_type`: input entry type,
    #      - `model`: the neural net model to be used by NeuralCoref. If set to True
    #         (default), a new instance will be created with `NeuralCoref.Model()`
    #         in NeuralCoref.from_disk() or NeuralCoref.from_bytes().
    #      - `cfg_inference`: A dict of configuration of inference. If set to an empty
    #         dict, the default configuration in NeuralCoref will be used. Available
    #         entries: `greedyness` (default 0.5), `max_dist` (default 50),
    #         `max_dist_match` (default 500), `blacklist` (default True),
    #         `store_scores` (default True), `conv_dict` (default None),

    #     Returns: A dictionary with the default config for this processor.
    #     """
    #     return {
    #         # TODO: remove unnecessaries
    #         "entry_type": "ft.onto.base_ontology.Document",
    #         "model": True,
    #         "cfg_inference": {},
    #     }

    @classmethod
    def default_configs(cls):
        r"""
        This defines a basic config structure for `CoreferenceProcessor`.

        Following are the keys for this dictionary:
         - `entry_type`: Input entry type. Default `"ft.onto.base_ontology.Document"`.
         - `model`: the neural net model to be used by NeuralCoref. If set to `True`
            (default), a new instance will be created with `NeuralCoref.Model()`
            in `NeuralCoref.from_disk()` or `NeuralCoref.from_bytes()`.
         - `greedyness`: TODO. Default `0.5`.
         - `max_dist`: TODO. Default `50`.
         - `max_dist_match`: TODO. Default `500`.
         - `blacklist`: TODO. Default `True`.
         - `store_scores`: TODO. Default `True`
         - `conv_dict`: TODO. Default `None`.

        Returns: A dictionary with the default config for this processor.
        """
        return {
            "entry_type": "ft.onto.base_ontology.Document",
            "model": True,
            "greedyness": 0.5,
            "max_dist": 50,
            "max_dist_match": 500,
            "blacklist": True,
            "store_scores": True,
            "conv_dict": None,
        }

    def expected_types_and_attributes(self):
        r"""
        Method to add user specified expected type which would be checked
        before running the processor if the pipeline is initialized with
        `enforce_consistency=True` or
        :meth:`~forte.pipeline.Pipeline.enforce_consistency` was enabled for
        the pipeline.
        """
        return {"ft.onto.base_ontology.Document": set()}

    def record(self, record_meta: Dict[str, Set[str]]):
        r"""
        Method to add output type record of `CoreferenceProcessor` which
        is `"ftx.medical.clinical_ontology.MedicalArticle"` with attribute
        `coref_groups` and `has_coref`
        to :attr:`forte.data.data_pack.Meta.record`.

        Args:
            record_meta: the field in the datapack for type record that need to
                fill in for consistency checking.
        """  # TODO: check docstring
        record_meta["ftx.medical.clinical_ontology.MedicalArticle"] = {
            "coref_groups",
            "has_coref",
        }
