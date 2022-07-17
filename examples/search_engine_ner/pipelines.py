from forte.data.readers import StringReader
from fortex.spacy import SpacyProcessor
from forte.data.data_pack import DataPack
from forte import Pipeline
from ft.onto.base_ontology import EntityMention
from typing import List


def process_data(text: str):

    pipeline: Pipeline = Pipeline[DataPack]()
    pipeline.set_reader(StringReader())
    pipeline.add(SpacyProcessor(), {"processors": ["sentence", "tokenize", "ner"]})

    for pack in pipeline.initialize().process_dataset(text):
        pack_ents: List[EntityMention] = list(pack.get(EntityMention))

        begin = [x.begin for x in pack_ents]
        end = [x.end for x in pack_ents]
        ner_type = [x.ner_type for x in pack_ents]

    res = []
    for i in range(len(begin)):
        res.append({"start": int(begin[i]), "end": int(end[i]), "label": ner_type[i]})

    return res
