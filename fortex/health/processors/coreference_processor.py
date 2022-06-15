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

from forte.common import Resources
from forte.common.configuration import Config
from forte.data.data_pack import DataPack
from forte.processors.base import PackProcessor

# from ft.onto.base_ontology import TODO
# from ftx.medical.clinical_ontology import TODO

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

    def set_up(self, configs: Config):
        pass
        # TODO

    def initialize(self, resources: Resources, configs: Config):
        super().initialize(resources, configs)
        self.set_up(configs)

    def _process(self, input_pack: DataPack):
        r"""
        TODO: Add docstring
        """
        pass
        # TODO    

    @classmethod
    def default_configs(cls):
        r"""
        TODO: Add docstring
        """
        return {
            # TODO
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
        is `"ftx.onto.clinical.TODO"` with attribute
        `TODO`
        to :attr:`forte.data.data_pack.Meta.record`.

        Args:
            record_meta: the field in the datapack for type record that need to
                fill in for consistency checking.
        """
        # TODO
