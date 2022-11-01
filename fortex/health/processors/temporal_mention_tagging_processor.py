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
Temporal Mention Tagger
"""
from typing import Dict, Set
import importlib

from transformers import pipeline
from forte.common import Resources
from forte.common.configuration import Config
from forte.data.data_pack import DataPack
from forte.processors.base import PackProcessor

from ftx.medical.clinical_ontology import TemporalTag


__all__ = [
    "TemporalMentionTaggingProcessor",
]

class TemporalMentionTaggingProcessor(PackProcessor):
    r"""
    Implementation of this TemporalMentionTaggingProcessor has
    been based on Temporal Mention Tagger pretained model (of huggingface transformers),  A rendition of it that exists on github has been referred to as well.
    Referred repository link:
    https://huggingface.co/models?sort=downloads&search=temporal
    """

    def __init__(self):
        super().__init__()
        self.extractor = None

    def set_up(self):
        device_num = self.configs["cuda_devices"]
        self.extractor = pipeline( 
            "ner", 
            model=self.configs.model_name,
            tokenizer=self.configs.model_name,
            framework="pt",
            device=device_num,
        )

    def initialize(self, resources: Resources, configs: Config):
        super().initialize(resources, configs)
        self.set_up()

    def _process(self, input_pack: DataPack):
        r"""
        TemporalMentionTaggingProcessor is done on the basis of
        using huggingface Transformer and the corresponding
        trained model for Temporal Mention Tagging
        """

        path_str, module_str = self.configs.entry_type.rsplit(".", 1)

        mod = importlib.import_module(path_str)
        entry = getattr(mod, module_str)
        for entry_specified in input_pack.get(entry_type=entry):
            result = self.extractor(inputs=entry_specified.text)
            words = [[result[0]["word"], result[0]["start"], result[0]["end"]]]
            for i in range(1, len(result)):
                if result[i]["index"] == result[i - 1]["index"] + 1:
                    words[-1][0] += " " + result[i]["word"]
                    words[-1][2] = result[i]["end"]
                else:
                    words.append(
                        [
                            result[i]["word"],
                            result[i]["start"],
                            result[i]["end"],
                        ]
                    )
            temporal_mentions = []
            for word, begin, end in words:
                temporal_context = TemporalTag(
                    pack=input_pack,
                    begin=begin,
                    end=end,
                )
                temporal_context.entity = word
                temporal_mentions.append(temporal_context)

    @classmethod
    def default_configs(cls):
        r"""
        This defines a basic config structure for `TemporalMentionTaggingProcessor`.
        Following are the keys for this dictionary:
         - `entry_type`: input entry type,
         - `model_name`: the huggingface transformer model name to be
                         used for classification,
        Returns: A dictionary with the default config for this processor.
        """
        return {
            "entry_type": "ft.onto.base_ontology.Document",
            "model_name": "satyaalmasian/temporal_tagger_BERT_tokenclassifier",
            "cuda_devices": -1,
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
        Method to add output type record of `TemporalMentionTaggingProcessor` which
        is `"ftx.medical.clinical_ontology.TemporalTag"` with attributes:
         `entity`
        """
        record_meta["ftx.medical.clinical_ontology.TemporalTag"] = {
            "entity",
        }
