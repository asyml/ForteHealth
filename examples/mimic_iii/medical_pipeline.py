import sys
from termcolor import colored

from forte.data.data_pack import DataPack
from forte.data.readers import StringReader
from forte.pipeline import Pipeline
from forte.processors.writers import PackIdJsonPackWriter
from ftx.onto.clinical import MedicalEntityMention
from ftx.medical.clinical_ontology import NegationContext

from ft.onto.base_ontology import (
    Token,
    Sentence,
    EntityMention,
)
from fortex.spacy import SpacyProcessor
from fortex.elastic import ElasticSearchPackIndexProcessor

from forte_medical.readers.mimic3_note_reader import Mimic3DischargeNoteReader
from forte_medical.processors.negation_context_analyzer import NegationContextAnalyzer

def main(input_path: str, output_path: str, max_packs: int = -1, singlePack: bool = True):
    pl = Pipeline[DataPack]()

    if singlePack is True:
        pl.set_reader(StringReader())
    else:
        pl.set_reader(
            Mimic3DischargeNoteReader(), config={"max_num_notes": max_packs}
        )
    configSpacy = {
        "processors": ["sentence", "tokenize", "pos", "ner", "umls_link"],
        "lang": "en_ner_bionlp13cg_md",
    }

    configNegation = {
        "negation_rules_path": "negex_triggers.txt",
    }

    pl.add(SpacyProcessor(), configSpacy)
    pl.add(ElasticSearchPackIndexProcessor())
    pl.add(NegationContextAnalyzer(), configNegation)

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

    text = (
        "Dr. Amanda, "
        "Medical Nutrition Therapy for Hyperlipidemia. "
        "Referral from: Julie Tester, RD, LD, CNSD "
        "Diet: General "
        "Daily Calorie needs (kcals): 1500 calories, assessed as HB + 20 for activity. "
        "Daily Protein needs: 40 grams, assessed as 1.0 g/kg. "
        "Pt has been on a 3-day calorie count and has had an average intake of 1100 calories. "
        "She was instructed to drink 2-3 cans of liquid supplement to help promote weight gain. "
        "She agrees with the plan and has my number for further assessment. May want a Resting "
        "Metabolic Rate as well. She takes an aspirin a day for knee pain."
    )

    if singlePack is True:
        pack = pl.process(text)
        showData(pack)
    else:
        packs = pl.process_dataset(input_path)
        for pack in packs:
            showData(pack)


def showData(pack: DataPack):
    for sentence in pack.get(Sentence):
        sent_text = sentence.text
        print(colored("Sentence:", "red"), sent_text, "\n")

        tokens = [
            (token.text, token.pos) for token in pack.get(Token, sentence)
        ]
        entities = [
            (entity.text, entity.ner_type)
            for entity in pack.get(EntityMention, sentence)
        ]

        medical_entities = []
        for entity in pack.get(MedicalEntityMention, sentence):
            for ent in entity.umls_entities:
                medical_entities.append(ent)

        for negation_context in pack.get(NegationContext, sentence):
            print (negation_context.text, negation_context.polarity)

        print(colored("Tokens:", "red"), tokens, "\n")
        print(colored("EntityMentions:", "red"), entities, "\n")
        print(colored("Medical Entity Mentions:", "cyan"), medical_entities, "\n")

        input(colored("Press ENTER to continue...\n", "green"))


main(sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4])
