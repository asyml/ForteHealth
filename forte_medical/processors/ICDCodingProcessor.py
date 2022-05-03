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
ICD Coding Processor
"""
from typing import Dict, List, Set
import importlib

from transformers import pipeline
from forte.common import Resources
from forte.common.configuration import Config
from forte.data.data_pack import DataPack
from forte.processors.base import PackProcessor

from ftx.medical.clinical_ontology import MedicalArticle


__all__ = [
    "ICDCodingProcessor",
]


class ICDCodingProcessor(PackProcessor):
    r"""
    Implementation of this ICDCodingProcessor has been based on  ICD Coding
    pretained model (of huggingface transformers),  A rendition of it that
    exists on github has been referred to as well.

    Referred repository link:
    https://huggingface.co/AkshatSurolia/ICD-10-Code-Prediction
    """

    def __init__(self):
        super().__init__()
        self.extractor = None

    def set_up(self):  # , configs: Config
        device_num = self.configs["cuda_devices"]
        self.extractor = pipeline(  # using Bert for SequenceClassification
            "sentiment-analysis",  # this is the actual pipeline name for Sequence-Classification
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
        ICDCodingProcessor is done on the basis of
        using huggingface Transformer and the corresponding
        trained model for ICDCode classification

        """

        path_str, module_str = self.configs.entry_type.rsplit(".", 1)

        mod = importlib.import_module(path_str)
        entry = getattr(mod, module_str)
        for entry_specified in input_pack.get(
            entry_type=entry
        ):  # entry_type=entry

            result = self.extractor(inputs=entry_specified.text)

            r0 = result[0]["label"]
            rt = MedicalArticle(pack=input_pack, begin=0, end=1)
            rt.icd_code = r0

    @classmethod
    def default_configs(cls):
        r"""
        This defines a basic config structure for `ICDCodingProcessor`.

        Following are the keys for this dictionary:
         - `entry_type`: input entry type,
         - `model_name`: the higgingface transformer model name to be
                         used for classification,

        Returns: A dictionary with the default config for this processor.
        """
        return {
            "entry_type": "ft.onto.base_ontology.Document",
            "attribute_name": "classification",
            "multi_class": True,
            "model_name": "AkshatSurolia/ICD-10-Code-Prediction",
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
        Method to add output type record of `ICDCodeProcessor` which
        is `"ftx.medical.clinical_ontology.MedicalArticle"` with attributes:
         `icd_version` and `icd_code`
        to :attr:`forte.data.data_pack.Meta.record`.

        Args:
            record_meta: the field in the datapack for type record that need to
                fill in for consistency checking.
        """
        record_meta["ftx.medical.clinical_ontology.MedicalArticle"] = {
            "icd_version",
            "icd_code",
        }
        if self.configs.entry_type in record_meta:
            record_meta[self.configs.entry_type].add(
                self.configs.attribute_name
            )
        else:
            record_meta[self.configs.entry_type] = {self.configs.attribute_name}
