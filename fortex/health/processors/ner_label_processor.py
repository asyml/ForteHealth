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
NER Labeling Processor
"""

from typing import Dict, Set
import spacy
from spacy.cli.download import download
from forte.data.data_pack import DataPack
from forte.processors.base import PackProcessor
from forte.common.configuration import Config
from forte.common.resources import Resources
from forte.common import ProcessExecutionException


from ftx.medical.clinical_ontology import Disease, Chemical


__all__ = [
    "NERLabelProcessor",
]

CUSTOM_SPACYMODEL_URL = {
    "en_core_sci_sm": "https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy"
    "/releases/v0.3.0/en_core_sci_sm-0.3.0.tar.gz",
    "en_core_sci_md": "https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy"
    "/releases/v0.3.0/en_core_sci_md-0.3.0.tar.gz",
    "en_core_sci_lg": "https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy"
    "/releases/v0.3.0/en_core_sci_lg-0.3.0.tar.gz",
    "en_ner_craft_md": "https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy"
    "/releases/v0.3.0/en_ner_craft_md-0.3.0.tar.gz",
    "en_ner_jnlpba_md": "https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy"
    "/releases/v0.3.0/en_ner_jnlpba_md-0.3.0.tar.gz",
    "en_ner_bc5cdr_md": "https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy"
    "/releases/v0.3.0/en_ner_bc5cdr_md-0.3.0.tar.gz",
    "en_ner_bionlp13cg_md": "https://s3-us-west-2.amazonaws.com/ai2-s2"
    "-scispacy/releases/v0.3.0/en_ner_bionlp13cg_md-0"
    ".3.0.tar.gz",
}


def load_lang_model(lang_model):
    # pylint: disable=import-outside-toplevel
    if lang_model in CUSTOM_SPACYMODEL_URL:
        # download ScispaCy model using URL
        import subprocess
        import sys
        import os
        import importlib

        download_url = CUSTOM_SPACYMODEL_URL[lang_model]
        command = [sys.executable, "-m", "pip", "install"] + [download_url]
        subprocess.run(
            command, env=os.environ.copy(), encoding="utf8", check=False
        )
        cls = importlib.import_module(lang_model)
        return cls.load()
    else:
        # Use spaCy download
        try:
            nlp = spacy.load(lang_model)
        except OSError:
            download(lang_model)
            nlp = spacy.load(lang_model)
    return nlp


class NERLabelProcessor(PackProcessor):
    r"""
    Implementation of this NERLabelProcessor has been based on spaCy
    pretained model. A rendition of it that exists on github has
    been referred to as well.

    Referred repository link:
    https://github.com/explosion/spaCy
    """

    def __init__(self):
        super().__init__()
        self.nlp = None

    def initialize(self, resources: Resources, configs: Config):
        super().initialize(resources, configs)
        self.nlp = load_lang_model(configs.lang)

    def _process(self, input_pack: DataPack):
        r"""
        NER Label processing is based on spaCy.
        """
        labels = self.configs.labels

        doc = input_pack.text

        # Do all process.
        if self.nlp is None:
            raise ProcessExecutionException(
                "The SpaCy pipeline is not initialized, maybe you "
                "haven't called the initialization function."
            )
        result = self.nlp(doc)

        for ent in result.ents:
            if "disease" in labels:
                if ent.label_ == "DISEASE":
                    Disease(
                        pack=input_pack, begin=ent.start_char, end=ent.end_char
                    )
            if "chemical" in labels:
                if ent.label_ == "CHEMICAL":
                    Chemical(
                        pack=input_pack, begin=ent.start_char, end=ent.end_char
                    )

    @classmethod
    def default_configs(cls):
        r"""
        This defines a basic config structure for `ICDCodingProcessor`.

        Following are the keys for this dictionary:
         - `labels`: ner labels

        Returns: A dictionary with the default config for this processor.
        """
        return {"labels": ["disease", "chemical"], "lang": "en_ner_bc5cdr_md"}

    def record(self, record_meta: Dict[str, Set[str]]):
        r"""

        Args:
            record_meta: the field in the datapack for type record that need to
                fill in for consistency checking.
        """
        record_meta["ft.onto.base_ontology.Disease"] = set()
        record_meta["ft.onto.base_ontology.Chemical"] = set()
