import json
import sys
import time

import yaml
from forte.common.configuration import Config
from forte.data.data_pack import DataPack
from forte.data.readers import PlainTextReader, RawDataDeserializeReader
from forte.pipeline import Pipeline
from forte.processors.writers import PackIdJsonPackWriter
from fortex.elastic import ElasticSearchPackIndexProcessor
from fortex.health.processors.icd_coding_processor import ICDCodingProcessor
from fortex.health.processors.negation_context_analyzer import \
    NegationContextAnalyzer
from fortex.huggingface import BioBERTNERPredictor
from fortex.nltk import NLTKNER, NLTKPOSTagger, NLTKSentenceSegmenter
from fortex.spacy import SpacyProcessor
from ft.onto.base_ontology import EntityMention, Sentence
from ftx.medical.clinical_ontology import (MedicalArticle,
                                           MedicalEntityMention,
                                           NegationContext)
from stave_backend.lib.stave_session import StaveSession

from mimic3_note_reader import Mimic3DischargeNoteReader
from utterance_searcher import LastUtteranceSearcher


def get_json(path: str):
    file_obj = open(path)
    data = json.load(file_obj)
    file_obj.close()
    return data


def update_stave_db(default_project_json, chat_project_json, chat_doc_json, config):
    project_id_base = 0
    with StaveSession(url=config.Stave.url) as session:
        session.login(username=config.Stave.username, password=config.Stave.pw)

        projects = session.get_project_list().json()
        project_names = [project["name"] for project in projects]

        if (
            default_project_json["name"] in project_names
            and chat_project_json["name"] in project_names
            ):

            base_project = [
                proj
                for proj in projects
                if proj["name"] == default_project_json["name"]
            ][0]
            return base_project["id"]

        resp1 = session.create_project(default_project_json)
        project_id_base = json.loads(resp1.text)["id"]

        resp2 = session.create_project(chat_project_json)
        project_id_chat = json.loads(resp2.text)["id"]

        chat_doc_json["project_id"] = project_id_chat
        doc_id = session.create_document(chat_doc_json)
        project_list = session.get_project_list().json()

    return project_id_base


def main(
    input_path: str, output_path: str, max_packs: int = -1, use_mimiciii_reader=1
    ):
    print("Starting demo pipeline example..")
    config = yaml.safe_load(open("clinical_config.yml", "r"))
    config = Config(config, default_hparams=None)
    print("Running pipeline...")
    pl = Pipeline[DataPack]()
    if use_mimiciii_reader == 1:
        pl.set_reader(
            Mimic3DischargeNoteReader(), config={"max_num_notes": max_packs}
            )
    else:
        pl.set_reader(PlainTextReader())

    pl.add(SpacyProcessor(), {"processors": ["sentence", "tokenize"]})
    pl.add(NLTKPOSTagger())
    pl.add(BioBERTNERPredictor(), config=config.BioBERTNERPredictor)
    pl.add(NegationContextAnalyzer())
    pl.add(
        ICDCodingProcessor(),
        {
            "entry_type": "ft.onto.base_ontology.Sentence",
        },
    )
    pl.add(
        ElasticSearchPackIndexProcessor(),
        {
            "indexer": {
                "other_kwargs": {"refresh": True},
            }
        },
    )
    pl.add(
        PackIdJsonPackWriter(),
        {
            "output_dir": output_path,
            "indent": 2,
            "overwrite": True,
            "drop_record": True,
            "zip_pack": False,
        },
    )

    pl.initialize()

    for idx, pack in enumerate(pl.process_dataset(input_path)):
        if (idx + 1) % 50 == 0:
            print(f"{time.strftime('%m-%d %H:%M')}: Processed {idx + 1} packs")

    default_project_json = get_json(config.viewer_project_json)
    chat_project_json = get_json(config.chat_project_json)
    chat_doc_json = get_json(config.chat_document_json)

    base_project_id = update_stave_db(
        default_project_json, chat_project_json, chat_doc_json, config
    )

    remote_pl = Pipeline[DataPack]()
    remote_pl.set_reader(RawDataDeserializeReader())
    remote_pl.add(
        LastUtteranceSearcher(),
        config={
            "query_result_project_id": base_project_id,
            "stave_db_path": config.LastUtteranceSearcher.stave_db_path,
            "url_stub": config.LastUtteranceSearcher.url,
        },
    )
    remote_pl.serve(
        port=config.Remote.port,
        input_format=config.Remote.input_format,
        service_name=config.Remote.service_name,
    )


main(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
