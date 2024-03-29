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
Unit tests for XrayImageReader
"""

import os
import unittest
from ddt import ddt, data

from forte.pipeline import Pipeline
from forte.data.data_pack import DataPack
from fortex.health.readers.xray_image_reader import XrayImageReader
import numpy as np
from PIL import Image


class XrayImageReaderDirPipelineTest(unittest.TestCase):
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

        self.expected_image_path = os.listdir(self.orig_image_pth)

        self.reader = XrayImageReader()
        self.pl = Pipeline[DataPack]()
        self.pl.set_reader(self.reader)
        self.pl.initialize()

    def test_reader(self):
        for pack in self.pl.process_dataset(self.orig_image_pth):
            self.assertTrue(
                pack.pack_name.split("/")[-1] in self.expected_image_path
            )


if __name__ == "__main__":
    unittest.main()
