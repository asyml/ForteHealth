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

# import MedicalArticle to get article data from data pack
from ftx.medical.clinical_ontology import MedicalArticle

# import mimic3 dataset
from fortex.health.readers.mimic3_note_reader import Mimic3DischargeNoteReader

# import ICD coding processor
from fortex.health.processors.icd_coding_processor import (
    ICDCodingProcessor,
)

def main(
    input_path: str, # path to input notes
    output_path: str, # path to output
    max_packs: int = -1, # max number of notes to read from mimic3 dataset
    use_mimic3_reader: bool = True, # read from mimic3 dataset or input_path
):
    # create a pipeline
    pl = Pipeline[DataPack]()

    # select reader: read from mimic3 dataset or from file
    if use_mimic3_reader is False:
        pl.set_reader(PlainTextReader())
    else:
        pl.set_reader(
            Mimic3DischargeNoteReader(), config={"max_num_notes": max_packs}
        )

    # load config
    config = Config(yaml.safe_load(open("config.yml", "r")), None)

    # add processors
    # use spacy for tokenizing
    pl.add(SpacyProcessor(), config.Spacy)
    # predict icd code
    pl.add(ICDCodingProcessor(), config.ICD)
    # add writer to save the output to the disk
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

    # initialize the pipeline before using it
    pl.initialize()

    # process data
    packs = pl.process_dataset(input_path)
    for pack in packs:
        showData(pack)

def showData(pack: DataPack):
    # show the processed data
    
    # The ICD processor predicts ICD code for each article.
    # The result is stored as article.icd_code.
    # The articles are packed into DataPack.
    # Therefore, we first extract articles from DataPack and then get their ICD codes.
    
    # extract ariticle
    for article in pack.get(MedicalArticle):
        # get original text
        article_text = article.text

        # get parsed tokens
        tokens = [
            (token.text, token.pos) for token in pack.get(Token, article)
        ]

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
# python icd_coding.py sample_data/ /path_to_sample_output 1000 True
# 
# Read from sample_data:
# python icd_coding.py sample_data/ /path_to_sample_output 1000 False
main(sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4].lower() == "true")
