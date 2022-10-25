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
XRAY_Processor Processor
"""
from typing import Dict
import PIL
from transformers import pipeline
from forte.data.data_pack import DataPack
from forte.common.resources import Resources
from forte.common.configuration import Config
from forte.processors.base import PackProcessor
from ft.onto.base_ontology import Classification


__all__ = [
    "XRAY_Processor",
]


class XRAY_Processor(PackProcessor):
    r"""
    Implementation of this XRAY_Processor has been based on the fine-tuned
    version of google/vit-base-patch16-224-in21k
    on the chest-xray-pneumonia dataset.

    The finetuned model nickmuchi/vit-finetuned-chest-xray-pneumonia (of huggingface transformers)
    achieves the following results on the evaluation set:

    Loss: 0.1271
    Accuracy: 0.9551

    Referred link:
    https://huggingface.co/nickmuchi/vit-finetuned-chest-xray-pneumonia#vit-finetuned-chest-xray-pneumonia
    """

    def __init__(self):
        super().__init__()
        self.extractor = None

    def set_up(self):

        device_num = self.configs["cuda_devices"]
        self.extractor = pipeline(
            "image-classification",
            model=self.configs.model_name,
            feature_extractor=self.configs.model_name,
            framework="pt",
            device=device_num,
        )

    def initialize(self, resources: Resources, configs: Config):
        super().initialize(resources, configs)
        self.set_up()

    def _process(self, input_pack: DataPack):
        r"""
        The model predicts the probablity score for
        the two classes 'PNEUMONIA' and 'NORMAL', based on
        an xray image input.

        """
        image_data = input_pack.image
        pil_img = PIL.Image.fromarray(image_data)
        out = self.extractor(pil_img)
        out_dict = {}
        for i in out:
            out_dict[i["label"]] = i["score"]
        class_labels: Classification = Classification(pack=input_pack)
        class_labels.classification_result = out_dict

    @classmethod
    def default_configs(cls):
        r"""
        This defines a basic config structure for `XRAY_Processor`.

        Following are the keys for this dictionary:
         - `model_name`: the higgingface transformer model name to be
                         used for classification,
         - `cuda_devices`: This the GPU device id, if set to "-1" CPU
                         will be used for the computation.

        Returns: A dictionary with the default config for this processor.
        """
        return {
            "model_name": "nickmuchi/vit-finetuned-chest-xray-pneumonia",
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
            "ft.onto.base_ontology.ImagePayload": [],
        }

    def record(self, record_meta: Dict[str]):
        r"""
        Method to add output type record of `XRAY_Processor` which
        is `ft.onto.base_ontology.Classification` with attribute `classification_result`
        to :attr:`forte.data.data_pack.Meta.record`.

        Args:
            record_meta: the field in the datapack for type record that need to
                fill in for consistency checking.
        """
        record_meta["ft.onto.base_ontology.Classification"] = {
            "classification_result",
        }
