import sys
import yaml
from termcolor import colored

from forte.common.configuration import Config
from forte.data.data_pack import DataPack
from forte.data.readers import PlainTextReader
from forte.pipeline import Pipeline
from forte.processors.writers import PackIdJsonPackWriter

from ft.onto.base_ontology import (
    Token,
)
from fortex.spacy import SpacyProcessor

from ftx.medical.clinical_ontology import MedicalArticle
from fortex.health.readers.mimic3_note_reader import Mimic3DischargeNoteReader
from fortex.health.processors.icd_coding_processor import (
    ICDCodingProcessor,
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

    config = Config(yaml.safe_load(open("config.yml", "r")), None)

    pl.add(SpacyProcessor(), config.Spacy)
    pl.add(ICDCodingProcessor(), config.ICD)
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
        showData(pack)


def showData(pack: DataPack):
    # The ICD processor predicts ICD code for each article.
    # The result is stored as article.icd_code.
    # The articles are packed into DataPack.
    # Therefore, we first extract articles from DataPack and then get their ICD codes.

    for article in pack.get(MedicalArticle):
        article_text = article.text
        tokens = [(token.text) for token in pack.get(Token, article)]

        # get the ICD code and its coding version
        icd_code = article.icd_code
        icd_version = article.icd_version

        print(colored("Article:", "red"), article_text, "\n")
        print(colored("Tokens:", "red"), tokens, "\n")
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
