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
Unit tests for XrayImageProcessor
"""

import os
import unittest
from ddt import ddt, data

from forte.pipeline import Pipeline
from forte.data.data_pack import DataPack
from fortex.health.readers.xray_image_reader import XrayImageReader
from fortex.health.processors.xray_image_processor import XrayImageProcessor
from ft.onto.base_ontology import Classification

import numpy as np
from PIL import Image


class XrayImageProcessorPipelineTest(unittest.TestCase):
    def setUp(self):
        self.orig_image_pth: str = os.path.abspath(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                os.pardir,
                os.pardir,
                os.pardir,
                os.pardir,
                "examples/xray/sample_data/",
            )
        )

        self.reader = XrayImageReader()
        self.pl = Pipeline[DataPack]()
        self.pl.set_reader(self.reader)
        self.pl.add(XrayImageProcessor())
        self.pl.initialize()

    def test_processor(self):
        for pack in self.pl.process_dataset(self.orig_image_pth):
            for output in pack.get(Classification):
                if "pneumonia" in pack.pack_name:
                    self.assertTrue(output.classification_result["PNEUMONIA"] >= 0.5)
                elif "normal" in pack.pack_name:
                    self.assertTrue(output.classification_result["NORMAL"] >= 0.5)
                else:
                    pass


if __name__ == "__main__":
    unittest.main()
