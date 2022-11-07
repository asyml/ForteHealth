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
    input_path: str,  # Path to mimic3 data if use_mimic3_reader=True else path to notes directory
    output_path: str,  # Path to output directory
):
    pl = Pipeline[DataPack]()
    pl.set_reader(PlainTextReader())

    # pl.add(
    #     SpacyProcessor(),
    #     {"processors": ["sentence"], "lang": "en_core_sci_sm"},
    # )
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
    # pl.add(
    #     PackIdJsonPackWriter(),
    #     {
    #         "output_dir": output_path,
    #         "indent": 2,
    #         "overwrite": True,
    #         "drop_record": True,
    #         "zip_pack": True,
    #     },
    # )

    pl.initialize()

    packs = pl.process_dataset(input_path)

    for pack in packs:
        for idx, abv_item in enumerate(pack.get(Abbreviation)):
            print(abv_item.long_form.text)


def show_data(pack: DataPack):
    # The ICD processor predicts ICD code for each article.
    # The result is stored as article.icd_code.
    # The articles are packed into DataPack.
    # Therefore, we first extract articles from DataPack and then get their ICD codes.

    for article in pack.get(MedicalArticle):
        article_text = article.text

        # get the ICD code and its coding version
        icd_code = article.icd_code
        icd_version = article.icd_version

        print(colored("Article:", "red"), article_text, "\n")
        print(colored(f"ICD-{icd_version} Code:", "cyan"), icd_code, "\n")

        input(colored("Press ENTER to continue...\n", "green"))


# Examples:
#
# Read from MIMIC3:
# python icd_coding.py /path/to/mimiciii/1.4/NOTEEVENTS.csv.gz /path_to_sample_output 1000 True
#
# Read from sample_data:
# python medical_text_understanding.py sample_data/ /path_to_sample_output 1000 False
# python medical_text_understanding.py sample_data/ .
main(sys.argv[1], sys.argv[2])
