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
XRAY Processor
"""

from forte.data.data_pack import DataPack
from forte.common.resources import Resources
from forte.common.configuration import Config
from forte.processors.base import PackProcessor
from transformers import AutoFeatureExtractor, AutoModelForImageClassification
from ft.onto.base_ontology import Classification
import torch

__all__ = [
    "XRAY_Processor",
]

class XRAY_Processor(PackProcessor):
    """
    An image processor for classification.
    """

    def initialize(self, resources: Resources, configs: Config):
        super().initialize(resources, configs)

        self.extractor = AutoFeatureExtractor.from_pretrained("nickmuchi/vit-finetuned-chest-xray-pneumonia")
        self.model = AutoModelForImageClassification.from_pretrained("nickmuchi/vit-finetuned-chest-xray-pneumonia")

    def _process(self, input_pack: DataPack):

        image_data = input_pack.image

        extract=self.extractor(image_data, return_tensors="pt")

        with torch.no_grad():
            logits = self.model(**extract).logits
            prob=torch.nn.functional.softmax(logits, dim=1)
        predicted_label = logits.argmax(-1).item()

        output = self.model.config.id2label[predicted_label]
        prob_cls=prob[0].numpy()[predicted_label]
        class_labels: Classification = Classification(
                pack=input_pack
            )
        class_labels.classification_result = {output:prob_cls}