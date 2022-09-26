# Copyright 2021 The Forte Authors. All Rights Reserved.
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

from typing import Any, Iterator
from forte.data.data_pack import DataPack
from forte.data.base_reader import PackReader
import numpy as np
from PIL import Image

class XrayImageReader(PackReader):
    r""":class:`ImageReader` is designed to read in an image file."""

    def __init__(self):
        super().__init__()
        self.Image = Image

    def _collect(self, image_path) -> Iterator[Any]:  # type: ignore
        r"""Should be called with param ``image_path`` which is a path to 
        the Image file.

        Args:
            image_path: path to the Image file.

        Returns: Image path
        """
        return image_path


    def _parse_pack(self, file_path: str) -> Iterator[DataPack]:
        pack: DataPack = DataPack()

        # Read in image data and store in DataPack
        img = self.Image.open(
            file_path)
        # coverts the image into RBG if we receive a grayscale image
        if img.mode == 'L':
            img = img.convert('RGB')
        pack.add_image(image=np.array(img))
        pack.pack_name = file_path

        yield pack
