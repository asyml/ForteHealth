import os

from forte.data.data_pack import DataPack
from fortex.health.readers.xray_image_reader import XrayImageReader
from fortex.health.processors.xray_image_processor import XrayImageProcessor
from ft.onto.base_ontology import Classification
from forte.pipeline import Pipeline

import numpy as np
from PIL import Image

# default folder name
img_folder = "sample_data"


def main(image_pth):
    pipeline = Pipeline[DataPack]()
    pipeline.set_reader(XrayImageReader())
    pipeline.add(XrayImageProcessor())
    pipeline.initialize()

    for datapack in pipeline.process_dataset(img_folder):
        for j in datapack.get(Classification):
            # printing the file name
            print(datapack.pack_name)
            # printing the classification result
            print(j.classification_result, end="\n\n")


if __name__ == "__main__":
    if sys.argv[0]:
        main(sys.argv[0])
    else:
        main(img_folder)
