import sys
from termcolor import colored

from forte.data.data_pack import DataPack
from forte.data.readers import PlainTextReader
from forte.pipeline import Pipeline

from ftx.medical.clinical_ontology import Hyponym, Abbreviation
from fortex.health.processors.scispacy_processor import (
    ScispaCyProcessor,
)

def main(
    input_path: str,
    process: str,
):
    pl = Pipeline[DataPack]()
    pl.set_reader(PlainTextReader())
    if process == "abbreviation":
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
    elif process == "hyponym":
        pl.add(
            ScispaCyProcessor(),
            {
                "entry_type": "ft.onto.base_ontology.Document",
                "model_name": "en_core_sci_sm",
                "pipe_name": "hyponym_detector",
                "prefer_gpu": True,
                "require_gpu": False,
                "gpu_id": 0,
            },
        )
    else:
        raise ValueError("""Please use hyponym or abbreviation as argument. e.g., 
            Abbreviation:
                python medical_text_understanding.py sample_data_abb/ abbreviation
            Hyponym detection:
                python medical_text_understanding.py sample_data_hyp/ hyponym""")

    pl.initialize()

    packs = pl.process_dataset(input_path)

    for pack in packs:
        if process == "abbreviation":
            print(colored("Input Sentence:", "blue"), colored( pack.text, "red"))
            for idx, abv_item in enumerate(pack.get(Abbreviation)):
                print(colored("Abbreviation:", "blue"), colored( abv_item.text, "green"))
                print(colored("Long form text:", "blue"), colored( abv_item.long_form.text, "green"), "\n")

        elif process == "hyponym":
            print(colored("Input Sentence:", "blue"), colored( pack.text, "red"))
            for idx, detected in enumerate(pack.get(Hyponym)):
                print(colored("hyponym_link:", "blue"), colored(detected.hyponym_link, "green"))
                print(colored("hypernym:", "blue"), colored(detected.general, "green"))
                print(colored("hyponym:", "blue"), colored(detected.specific, "green")+"\n\n")
# Examples:
'''
Read from sample_data:
Abbreviation:
    python medical_text_understanding.py sample_data_abb/ abbreviation
Hyponym detection:
    python medical_text_understanding.py sample_data_hyp/ hyponym
'''
main(sys.argv[1], sys.argv[2])
