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
from typing import Dict, Set
import importlib

import neuralcoref

from forte.common import Resources, ProcessExecutionException
from forte.common.configuration import Config
from forte.data.data_pack import DataPack
from forte.processors.base import PackProcessor

from ft.onto.base_ontology import CoreferenceGroup
from ftx.medical.clinical_ontology import MedicalArticle

from fortex.spacy.spacy_processors import load_lang_model

__all__ = [
    "CoreferenceProcessor",
]


class CoreferenceProcessor(PackProcessor):
    r"""
    Implementation of this CoreferenceProcessor has been based on huggingface
    NeuralCoref. You can find more details in the original repo.

    Note that the NeuralCoref package from PyPI uses a dated spaCy
    version (2.1), which can cause segmentation fault with the spaCy we use (2.3).
    Please install NeuralCoref by building from source.

    Referred repository link:
    https://github.com/huggingface/neuralcoref
    """

    def __init__(self):
        super().__init__()
        self.spacy_nlp = None

    def set_up(self, configs: Config):
        self.spacy_nlp = load_lang_model(configs.lang)

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
        Coreference resolution is done by
        a spaCy pipeline with `NeuralCoref` added.

        Then we translate the output to `CoreferenceGroup` and
        `MedicalEntityMention`
        """

        def load_module(string):
            path_str, module_str = string.rsplit(".", 1)
            mod = importlib.import_module(path_str)
            return getattr(mod, module_str)

        # Default: Document
        entry_type = load_module(self.configs.entry_type)

        # Default: MedicalEntityMention
        mention_type = load_module(self.configs.mention_type)

        for entry_specified in input_pack.get(entry_type=entry_type):
            result = self.spacy_nlp(entry_specified.text)

            article = MedicalArticle(
                pack=input_pack,
                begin=entry_specified.span.begin,
                end=entry_specified.span.end,
            )

            if not result._.has_coref:
                article.has_coref = False
                article.coref_groups = []
                article.coref_resolved = result._.coref_resolved
                article.coref_scores = {}
            else:
                article.has_coref = True
                article.coref_groups = []
                article.coref_resolved = result._.coref_resolved
                article.coref_scores = result._.coref_scores
                for cluster in result._.coref_clusters:

                    mentions = []
                    for mention in cluster.mentions:
                        mention = mention_type(
                            input_pack,
                            mention.start_char,
                            mention.end_char,
                        )
                        mentions.append(mention)

                    group = CoreferenceGroup(input_pack)
                    group.add_members(mentions)

                    article.coref_groups.append(group)

    @classmethod
    def default_configs(cls):
        r"""
        This defines a basic config structure for `CoreferenceProcessor`.

        Following are the keys for this dictionary:
         - `entry_type`: Input entry type. Default: `"ft.onto.base_ontology.Document"`.
         - `mention_type`: Output mention type.
            Default: `"ftx.medical.clinical_ontology.MedicalEntityMention"`.
            It can also be set to `"ft.onto.base_ontology.EntityMention"`.
         - `model`: the neural net model to be used by NeuralCoref. If set to `True`,
            a new instance will be created with `NeuralCoref.Model()`. Default: `True`.
            in `NeuralCoref.from_disk()` or `NeuralCoref.from_bytes()`.
         - `greedyness` (`float`): A number between 0 and 1 determining how greedy
            the model is about making coreference decisions
            (more greedy means more coreference links). Default: `0.5`.
         - `max_dist` (`int`): How many mentions back to look when considering possible
            antecedents of the current mention. Decreasing the value will cause
            the system to run faster but less accurately. Default: `50`.
         - `max_dist_match` (`int`): The system will consider linking the current mention
            to a preceding one further than max_dist away if they share a noun or
            proper noun. In this case, it looks max_dist_match away instead. Default: `500`.
         - `blacklist` (`bool`): Should the system resolve coreferences for pronouns in the
            following list: ["i", "me", "my", "you", "your"]. Default `True`.
         - `store_scores` (`bool`): Should the system store the scores for the coreferences
            in annotations. Default: `True`
         - `conv_dict` (`dict(str, list(str))`): A conversion dictionary that you can use
            to replace the embeddings of rare words (keys) by an average of the embeddings
             of a list of common words (values). Ex: `conv_dict={"Angela": ["woman", "girl"]}`
             will help resolving coreferences for Angela by using the embeddings for the more
             common woman and girl instead of the embedding of Angela.
             This currently only works for single words (not for words groups). Default: `None`.

        Returns: A dictionary with the default config for this processor.
        """
        return {
            "entry_type": "ft.onto.base_ontology.Document",
            "mention_type": "ftx.medical.clinical_ontology.MedicalEntityMention",
            "lang": "en_core_web_sm",
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
        `coref_groups`, `has_coref`, `coref_scores`, and `coref_resolved`
        to :attr:`forte.data.data_pack.Meta.record`.

        Args:
            record_meta: the field in the datapack for type record that need to
                fill in for consistency checking.
        """
        record_meta["ftx.medical.clinical_ontology.MedicalArticle"] = {
            "coref_groups",
            "has_coref",
            "coref_scores",
            "coref_resolved",
        }
