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
<<<<<<< HEAD
SciSpacy Processor
"""
from typing import Dict, Set
import importlib
import re

import spacy
from timexy import Timexy
=======
Temporal Mention Tagger and Normalizer
"""
from typing import Dict, Set
import importlib

from transformers import pipeline
>>>>>>> 5be02e5 (Add tagging processor)
from forte.common import Resources
from forte.common.configuration import Config
from forte.data.data_pack import DataPack
from forte.processors.base import PackProcessor

<<<<<<< HEAD
from ftx.medical.clinical_ontology import NormalizedTemporalForm

__all__ = [
    "TemporalMentionNormalizingProcessor",
]


class TemporalMentionNormalizingProcessor(PackProcessor):
    r"""
    Implementation of this TemporalMentionNormalizingProcessor has
    been based on Timexy rule based model (based on spacy),  A rendition of it that exists on github has been referred
    to as well.

    Referred repository link:
    https://github.com/paulrinckens/timexy
=======
from ftx.medical.clinical_ontology import TemporalTag, NormalizedTemporalForm


__all__ = [
    "TemporalMentionTaggingAndNormalizingProcessor",
]


class TemporalMentionTaggingAndNormalizingProcessor(PackProcessor):
    r"""
    Implementation of this TemporalMentionTaggingAndNormalizingProcessor has
    been based on Temporal Mention Tagger pretained model (of huggingface
    transformers),  A rendition of it that exists on github has been referred
    to as well.
    Referred repository link:
    https://huggingface.co/models?sort=downloads&search=temporal
>>>>>>> 5be02e5 (Add tagging processor)
    """

    def __init__(self):
        super().__init__()
        self.extractor = None

<<<<<<< HEAD
    def set_up(self):
        if self.configs.require_gpu:
            spacy.require_gpu(self.configs.gpu_id)
        if self.configs.prefer_gpu:
            spacy.prefer_gpu(self.configs.gpu_id)
        self.extractor = spacy.load(self.configs.model_name)
        self.extractor.add_pipe(self.configs.pipe_name, before="ner")
=======
    def set_up(self):  # , configs: Config
        device_num = self.configs["cuda_devices"]
        self.extractor = pipeline(  # using transformer for token classification Sequence2Sequence
            "ner",  # this is the actual pipeline name for token-Classification
            model=self.configs.model_name,  # satyaalmasian/temporal_tagger_BERT_tokenclassifier
            tokenizer=self.configs.model_name,
            framework="pt",
            device=device_num,
        )
>>>>>>> 5be02e5 (Add tagging processor)

    def initialize(self, resources: Resources, configs: Config):
        super().initialize(resources, configs)
        self.set_up()

    def _process(self, input_pack: DataPack):
        r"""
<<<<<<< HEAD
        ScispaCyProcessor is done on the basis of
        using SciSpacy and the corresponding
        trained model for Hyponym, Abbreviation

        """
        path_str, module_str = self.configs.entry_type.rsplit(".", 1)
        mod = importlib.import_module(path_str)
        entry = getattr(mod, module_str)
        for entry_specified in input_pack.get(entry_type=entry):
            doc = self.extractor(entry_specified.text)
            normalized_text = []
            for e in doc.ents:
                print(f"{e.text}\t{e.label_}\t{e.kb_id_}")
                tmp_txt = NormalizedTemporalForm(
                    pack=input_pack, begin=0, end=len(e.text)
                )
                m = re.findall(r'type="(.*?)"', e.kb_id_)
                if m:
                    tmp_txt.type = m[0]
                m = re.findall(r'value="(.*?)"', e.kb_id_)
                if m:
                    tmp_txt.value = m[0]
                normalized_text.append(tmp_txt)
=======
        TemporalMentionTaggingAndNormalizingProcessor is done on the basis of
        using huggingface Transformer and the corresponding
        trained model for Temporal Mention Tagging And Normalizing
        """

        path_str, module_str = self.configs.entry_type.rsplit(".", 1)

        mod = importlib.import_module(path_str)
        entry = getattr(mod, module_str)
        for entry_specified in input_pack.get(entry_type=entry):
            result = self.extractor(inputs=entry_specified.text)
            print("here", result)
            words = [[result[0]["word"], result[0]["start"], result[0]["end"]]]
            for i in range(1,len(result)):
                if result[i]["index"] == result[i-1]["index"] + 1:
                    words[-1][0] += " " + result[i]["word"]
                    words[-1][2] = result[i]["end"]
                else:
                    words.append([result[i]["word"], result[i]["start"], result[i]["end"]])
            print(words)
            temporal_mention = result[0]["word"]
            #print("temporal", temporal_mention)
            temporal_mentions = []
            for word, begin, end in words:
                temporal_context = TemporalTag(
                    pack=input_pack,
                    begin=begin,
                    end=end,
                )
                temporal_context.entity = word
                temporal_mentions.append(temporal_context)
            print(len(temporal_mentions))
>>>>>>> 5be02e5 (Add tagging processor)

    @classmethod
    def default_configs(cls):
        r"""
<<<<<<< HEAD
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

=======
        This defines a basic config structure for `ICDCodingProcessor`.
        Following are the keys for this dictionary:
         - `entry_type`: input entry type,
         - `model_name`: the higgingface transformer model name to be
                         used for classification,
>>>>>>> 5be02e5 (Add tagging processor)
        Returns: A dictionary with the default config for this processor.
        """
        return {
            "entry_type": "ft.onto.base_ontology.Document",
<<<<<<< HEAD
            "model_name": "en_core_sci_sm",
            "pipe_name": "abbreviation_detector",
            "prefer_gpu": True,
            "require_gpu": False,
            "gpu_id": 0,
=======
            "attribute_name": "classification",
            "multi_class": True,
            "model_name": "AkshatSurolia/ICD-10-Code-Prediction",
            "cuda_devices": -1,
>>>>>>> 5be02e5 (Add tagging processor)
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
<<<<<<< HEAD
            self.configs.entry_type: set(),
=======
            "ft.onto.base_ontology.Document": set(),
            "forte.data.ontology.top.Annotation": set(),
>>>>>>> 5be02e5 (Add tagging processor)
        }

    def record(self, record_meta: Dict[str, Set[str]]):
        r"""
<<<<<<< HEAD
        Method to add output type record of `ScispaCyProcessor` which
        is `"ftx.medical.clinical_ontology.hyponym"` with attributes:
         `hyponym_link`
        to :attr:`forte.data.data_pack.Meta.record`.

=======
        Method to add output type record of `ICDCodeProcessor` which
        is `"ftx.medical.clinical_ontology.MedicalArticle"` with attributes:
         `icd_version` and `icd_code`
        to :attr:`forte.data.data_pack.Meta.record`.
>>>>>>> 5be02e5 (Add tagging processor)
        Args:
            record_meta: the field in the datapack for type record that need to
                fill in for consistency checking.
        """
<<<<<<< HEAD
        record_meta["ftx.medical.clinical_ontology.NormalizedTemporalForm"] = {
            "type",
            "value",
=======
        record_meta["ftx.medical.clinical_ontology.TemporalTag"] = {
            "entity",
        }
        record_meta["ftx.medical.clinical_ontology.NormalizedTemporalForm"] = {
            "type",
            "value"
>>>>>>> 5be02e5 (Add tagging processor)
        }
