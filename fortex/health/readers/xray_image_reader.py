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
"""This class is designed to read Xray images from given image path.

    For more information for the dataset, visit:
      https://data.mendeley.com/datasets/jctsfj2sfn/1
    """
import os
from typing import Any, Iterator
from forte.data.data_pack import DataPack
from forte.data.base_reader import PackReader
from forte.data.data_utils_io import dataset_path_iterator
import numpy as np
from PIL import Image


class XrayImageReader(PackReader):
    r""":class:`ImageReader` is designed to read image files from a given folder."""

    def __init__(self):
        super().__init__()
        self.Image = Image

    def _collect(self, image_directory) -> Iterator[Any]:
        r"""Should be called with param ``image_directory`` which is a path to a
        folder containing image files.

        Args:
            Image_directory: Image directory containing the files.

        Returns: Iterator over paths to image files
        """
        return dataset_path_iterator(image_directory, self.configs.file_ext)

    def _cache_key_function(self, image_file: str) -> str:
        return os.path.basename(image_file)

    def _parse_pack(self, file_path: str) -> Iterator[DataPack]:
        pack: DataPack = DataPack()

        # Read in image data and store in DataPack
        img = self.Image.open(file_path, **(self.configs.read_kwargs or {}))
        if img.mode == "L":
            img = img.convert("RGB")
        pack.add_image(image=np.array(img))
        pack.pack_name = file_path

        yield pack

    @classmethod
    def default_configs(cls):
        r"""This defines a basic configuration structure for image reader.

        Here:

          - file_ext (str): The file extension to find the target files
             under a specific directory path. Default value is ".jpeg".

          - read_kwargs (dict): A dictionary containing all the keyword
             arguments for `PIL.Image` method. For details, refer to
             https://pillow.readthedocs.io/en/stable/reference/Image.html
             Default value is None.

        Returns: The default configuration of Image reader.
        """
        return {"file_ext": ".jpeg", "read_kwargs": None}
