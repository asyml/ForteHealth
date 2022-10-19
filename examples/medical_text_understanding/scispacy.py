import sys
from termcolor import colored

from forte.data.data_pack import DataPack
from forte.data.readers import PlainTextReader
from forte.pipeline import Pipeline
from forte.processors.writers import PackIdJsonPackWriter

from ft.onto.base_ontology import (
    Token,
)
from fortex.spacy import SpacyProcessor

from ftx.medical.clinical_ontology import Hyponym, Abbreviation, Phrase
from fortex.health.processors.scispacy_processor import (
    ScispaCyProcessor,
)


def main(
    input_path: str,  # Path to mimic3 data if use_mimic3_reader=True else path to notes directory
    output_path: str,  # Path to output directory
    max_packs: int = -1,  # Max number of notes to read from mimic3 dataset. Set to -1 to read all.
    use_mimic3_reader: bool = True,  # Read from mimic3 dataset or plain text
):
    pl = Pipeline[DataPack]()

    if use_mimic3_reader is False:
        pl.set_reader(PlainTextReader())
    else:
        pl.set_reader(Mimic3DischargeNoteReader(), config={"max_num_notes": max_packs})

    pl.add(
        SpacyProcessor(),
        {"processors": ["sentence"], "lang": "en_ner_bionlp13cg_md"},
    )
    pl.add(
        ICDCodingProcessor(),
        {
            "entry_type": "ft.onto.base_ontology.Document",
            "attribute_name": "classification",
            "multi_class": True,
            "model_name": "AkshatSurolia/ICD-10-Code-Prediction",  # You can use other ICD predictors here.
            "cuda_devices": -1,
        },
    )
    pl.add(
        PackIdJsonPackWriter(),
        {
            "output_dir": output_path,
            "indent": 2,
            "overwrite": True,
            "drop_record": True,
            "zip_pack": True,
        },
    )

    pl.initialize()

    packs = pl.process_dataset(input_path)
    for pack in packs:
        show_data(pack)


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
# python icd_coding.py sample_data/ /path_to_sample_output 1000 False
main(sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4].lower() == "true")
