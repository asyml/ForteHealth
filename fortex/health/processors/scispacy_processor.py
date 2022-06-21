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
        self.extractor = spacy.load(
            self.configs.model_name
        )
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
        for entry_specified in input_pack.get(entry_type=entry):

            doc = self.extractor(entry_specified.text)

            if self.configs.pipe_name == "abbreviation_detector":
                print("Abbreviation", "\t", "Definition")
                list_of_abrvs = []
                for abrv in doc._.abbreviations:
                    print(
                        f"{abrv} \t ({abrv.start}, {abrv.end}) {abrv._.long_form}"
                    )
                    tmpAbrv = Abbreviation(
                        pack=input_pack, begin=abrv.start, end=abrv.end
                    )
                    tmpAbrv.long_form = abrv._.long_form
                    list_of_abrvs.append(tmpAbrv)

            else:
                print(doc._.hearst_patterns)
                for item in doc._.hearst_patterns:
                    hlink = Hyponym(pack=input_pack)
                    hlink.hyponym_link = item[0]
                    general_phase = Phrase(pack=input_pack, begin=item[1].start, end=item[1].end)
                    hlink.parent = general_phase
                    specific_phase = Phrase(pack=input_pack, begin=item[2].start, end=item[2].end)
                    hlink.child = specific_phase

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
            "model_name": "en_core_sci_sm",
            "pipe_name": "abbreviation_detector",
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
        record_meta["ftx.medical.clinical_ontology.Abbreviation"] = {
            "long_form",
        }
        record_meta["ftx.medical.clinical_ontology.hyponym"] = {
            "hyponym_link",
            "ParentType",
            "ChildType",
        }

        if self.configs.entry_type in record_meta:
            record_meta[self.configs.entry_type].add(
                self.configs.attribute_name
            )
        else:
            record_meta[self.configs.entry_type] = {self.configs.attribute_name}