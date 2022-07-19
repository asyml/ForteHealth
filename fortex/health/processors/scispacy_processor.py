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
SciSpacy Processor
"""
from typing import Dict, Set
import importlib

import spacy
from forte.common import Resources
from forte.common.configuration import Config
from forte.data.data_pack import DataPack
from forte.processors.base import PackProcessor

# pylint: disable=unused-import
from scispacy.abbreviation import AbbreviationDetector
from scispacy.hyponym_detector import HyponymDetector

from ftx.medical.clinical_ontology import Hyponym, Abbreviation, Phrase

__all__ = [
    "ScispaCyProcessor",
]


class ScispaCyProcessor(PackProcessor):
    r"""
    Implementation of this ScispaCyProcessor has been based on ScispaCy
    pretained models (based on spacy),  A rendition of it that
    exists on github has been referred to as well.

    Referred repository link:
    https://pythonlang.dev/repo/allenai-scispacy/
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
        if self.configs.pipe_name == "abbreviation_detector":
            self.extractor.add_pipe(self.configs.pipe_name)
        else:  # hyponym
            self.extractor.add_pipe(
                self.configs.pipe_name, last=True, config={"extended": False}
            )

    def initialize(self, resources: Resources, configs: Config):
        super().initialize(resources, configs)
        self.set_up()

    def _process(self, input_pack: DataPack):
        r"""
        ScispaCyProcessor is done on the basis of
        using SciSpacy and the corresponding
        trained model for Hyponym, Abbreviation

        """

        path_str, module_str = self.configs.entry_type.rsplit(".", 1)
        mod = importlib.import_module(path_str)
        entry = getattr(mod, module_str)
        # entry = get_class(class_name=module_str, module_paths=path_str)
        for entry_specified in input_pack.get(entry_type=entry):

            doc = self.extractor(entry_specified.text)

            if self.configs.pipe_name == "abbreviation_detector":
                list_of_abrvs = []
                for abrv in doc._.abbreviations:
                    tmp_abrv = Abbreviation(
                        pack=input_pack, begin=abrv.start, end=abrv.end
                    )
                    tmp_abrv.long_form = abrv._.long_form
                    list_of_abrvs.append(tmp_abrv)

            else:
                for item in doc._.hearst_patterns:
                    general_concept: Phrase = Phrase(
                        pack=input_pack, begin=item[1].start, end=item[1].end
                    )
                    specific_concept = Phrase(
                        pack=input_pack, begin=item[2].start, end=item[2].end
                    )
                    hlink = Hyponym(
                        pack=input_pack,
                        parent=general_concept,
                        child=specific_concept,
                    )
                    hlink.hyponym_link = item[0]

    @classmethod
    def default_configs(cls):
        r"""
        This defines a basic config structure for `ScispaCyProcessor`.

        Following are the keys for this dictionary:
         - `entry_type`: should be ft.onto.base_ontology.Document
         - `model_name`: the scispaCy model name to be
                         used for classification, please refer to :
                         https://pythonlang.dev/repo/allenai-scispacy/
                         "Available models" sections for detail
         - `pipe_name`: the Spacy model pipe name for
                         classification, only 2 options here:
                         abbreviation_detector or hyponym_detector
         - `prefer_gpu`: the flag if prefer using gpu
         - `require_gpu`: the flag if require using gpu
         - `gpu_id`: the id of gpu

        Returns: A dictionary with the default config for this processor.
        """
        return {
            "entry_type": "ft.onto.base_ontology.Document",
            "model_name": "en_core_sci_sm",
            "pipe_name": "abbreviation_detector",
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
            self.configs.entry_type: set(),
        }

    def record(self, record_meta: Dict[str, Set[str]]):
        r"""
        Method to add output type record of `ScispaCyProcessor` which
        is `"ftx.medical.clinical_ontology.hyponym"` with attributes:
         `hyponym_link`
        to :attr:`forte.data.data_pack.Meta.record`.

        Args:
            record_meta: the field in the datapack for type record that need to
                fill in for consistency checking.
        """
        record_meta["ftx.medical.clinical_ontology.Abbreviation"] = {
            "long_form",
        }
        record_meta["ftx.medical.clinical_ontology.Hyponym"] = {
            "hyponym_link",
            "parent",
            "child",
        }

        if self.configs.entry_type in record_meta:
            record_meta[self.configs.entry_type].add(
                self.configs.attribute_name
            )
        else:
            record_meta[self.configs.entry_type] = {self.configs.attribute_name}
