# %%
import sys
import yaml
# missing package: termcolor
from termcolor import colored

from forte.common.configuration import Config
from forte.data.data_pack import DataPack
from forte.data.readers import PlainTextReader
from forte.pipeline import Pipeline
from forte.processors.writers import PackIdJsonPackWriter
from ftx.medical.clinical_ontology import NegationContext, MedicalEntityMention, MedicalArticle

from ft.onto.base_ontology import (
    Token,
    Sentence,
    EntityMention,
)
from fortex.spacy import SpacyProcessor

from fortex.health.readers.mimic3_note_reader import Mimic3DischargeNoteReader
from fortex.health.processors.negation_context_analyzer import (
    NegationContextAnalyzer,
)

from fortex.health.processors.icd_coding_processor import (
    ICDCodingProcessor,
)

# %%
def main(
    input_path: str,
    output_path: str,
    max_packs: int = -1,
    use_mimic3_reader: bool = True,
):
    pl = Pipeline[DataPack]()

    if use_mimic3_reader is False:
        pl.set_reader(PlainTextReader())
    else:
        pl.set_reader(
            Mimic3DischargeNoteReader(), config={"max_num_notes": max_packs}
        )

    config = Config(yaml.safe_load(open("config.yml", "r")), None)
    pl.add(SpacyProcessor(), config.Spacy)
    pl.add(NegationContextAnalyzer(), config.Negation)
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

# %%
def showData(pack: DataPack):
    for article in pack.get(MedicalArticle):
        article_text = article.text
        tokens = [
            (token.text, token.pos) for token in pack.get(Token, article)
        ]
        icd_code = article.icd_code
        
        print(colored("Article:", "red"), article_text, "\n")

        print(colored("Tokens:", "red"), tokens, "\n")
        print(
            colored("ICD Code:", "cyan"),
            icd_code,
            "\n",
        )

        input(colored("Press ENTER to continue...\n", "green"))

#%% $$

# Example: 
# python medical_pipeline.py sample_data/ /path_to_sample_output 1000 False
main(sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4].lower() == "true")

# %%
