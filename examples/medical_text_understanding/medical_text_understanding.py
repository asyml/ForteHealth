import sys
from termcolor import colored

from forte.data.data_pack import DataPack
from forte.data.readers import PlainTextReader
from forte.pipeline import Pipeline
from forte.processors.writers import PackIdJsonPackWriter

from ft.onto.base_ontology import (
    Token,
)

from ftx.medical.clinical_ontology import Hyponym, Abbreviation, Phrase
# from fortex.health.processors.scispacy_processor import (
#     ScispaCyProcessor,
# )

import sys
sys.path.append("/Users/nikhil.ranjan/Desktop/ForteHealth/fortex/health/processors")
from scispacy_processor import (
    ScispaCyProcessor,
)

def main(
    input_path: str,
):
    pl = Pipeline[DataPack]()
    pl.set_reader(PlainTextReader())
    pl.add(
        ScispaCyProcessor(),
        {
            "entry_type": "ft.onto.base_ontology.Document",
            "model_name": "en_core_sci_sm",
            "pipe_name": "abbreviation_detector",
            "prefer_gpu": True,
            "require_gpu": False,
            "gpu_id": 0,
        },
    )

    pl.initialize()

    packs = pl.process_dataset(input_path)

    for pack in packs:
        for idx, abv_item in enumerate(pack.get(Abbreviation)):
            print(colored("Long form text:", "red"), colored( abv_item.long_form.text, "blue"), "\n")

# Examples:
# Read from sample_data:
# python medical_text_understanding.py sample_data/
main(sys.argv[1])
