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
Temporal Mention Normalizer
"""
from typing import Dict, Set
import importlib
import re

import spacy

# pylint: disable=unused-import
from timexy import Timexy

from forte.common import Resources
from forte.common.configuration import Config
from forte.data.data_pack import DataPack
from forte.processors.base import PackProcessor

from ftx.medical.clinical_ontology import NormalizedTemporalForm

__all__ = [
    "TemporalMentionNormalizingProcessor",
]


class TemporalMentionNormalizingProcessor(PackProcessor):
    r"""
    Implementation of this TemporalMentionNormalizingProcessor has
    been based on Timexy rule based model (based on spacy), A
    rendition of it that exists on github has been referred
    to as well.

    Referred repository link:
    https://github.com/paulrinckens/timexy
    """

    def __init__(self):
        super().__init__()
        self.extractor = None

    def set_up(self):
        if self.configs.require_gpu:
            spacy.require_gpu(self.configs.gpu_id)
        if self.configs.prefer_gpu:
            spacy.prefer_gpu(self.configs.gpu_id)
        self.extractor = spacy.load(self.configs.model_name)
        self.extractor.add_pipe(self.configs.pipe_name, before="ner")

    def initialize(self, resources: Resources, configs: Config):
        super().initialize(resources, configs)
        self.set_up()

    def _process(self, input_pack: DataPack):
        r"""
        TemporalMentionNormalizingProcessor is done on the basis
        of using spacy, timexy and the corresponding trained model
        for en_web_sm
        """
        path_str, module_str = self.configs.entry_type.rsplit(".", 1)
        mod = importlib.import_module(path_str)
        entry = getattr(mod, module_str)
        for entry_specified in input_pack.get(entry_type=entry):
            doc = self.extractor(entry_specified.text)
            normalized_text = []
            for entities in doc.ents:
                tmp_txt = NormalizedTemporalForm(
                    pack=input_pack, begin=0, end=len(entities.text)
                )
                matches = re.findall(r'type="(.*?)"', entities.kb_id_)
                if matches:
                    tmp_txt.type = matches[0]
                matches = re.findall(r'value="(.*?)"', entities.kb_id_)
                if matches:
                    tmp_txt.value = matches[0]
                normalized_text.append(tmp_txt)

    @classmethod
    def default_configs(cls):
        r"""
        Following are the keys for this dictionary:
         - `entry_type`: should be ft.onto.base_ontology.Document
         - `model_name`: the spaCy model name to be
                         used for classification, please refer to :
                         https://spacy.io/usage/models
         - `pipe_name`: the Spacy model pipe name for
                         normalization, here:
                         timexy
        Returns: A dictionary with the default config for this processor.
        """
        return {
            "entry_type": "ft.onto.base_ontology.Document",
            "model_name": "en_core_web_sm",
            "pipe_name": "timexy",
            "prefer_gpu": True,
            "require_gpu": False,
            "gpu_id": 0,
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
            "ft.onto.base_ontology.Document": set(),
            "forte.data.ontology.top.Annotation": set(),
        }

    def record(self, record_meta: Dict[str, Set[str]]):
        r"""
        Method to add output type record of `TemporalMentionNormalizingProcessor` which
        is `"ftx.medical.clinical_ontology.NormalizedTemporalForm"` with attributes:
         `entity`
        to :attr:`forte.data.data_pack.Meta.record`.
        """
        record_meta["ftx.medical.clinical_ontology.NormalizedTemporalForm"] = {
            "type",
            "value",
        }
