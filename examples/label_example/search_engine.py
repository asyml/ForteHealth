import sqlite3
from typing import List
import streamlit as st
from forte.common.configuration import Config
import yaml
from elasticsearch import Elasticsearch
from search_utils import all_search, index_search
from sqlite_utils import create_links, sqlite_insert, get_json, update_stave_db
import templates


def main():
    st.set_page_config(page_title="ForteHealth_Search_Engine", layout="wide")

    es = Elasticsearch(hosts=["http://localhost:9200/"])
    INDEX = "elastic_indexer"

    config = yaml.safe_load(open("stave_config.yml", "r"))
    config = Config(config, default_hparams=None)

    default_project_json = get_json("default_onto_project.json")

    base_project_id = update_stave_db(default_project_json, config)

    st.title("Search the MIMIC III Data...")
    search = st.text_input("Enter search words:")

    if not search:
        records = {}
        results = all_search(es, INDEX)
        hits = results["hits"]["hits"]

        conn = sqlite3.connect(config.Stave.stave_db_path)
        answers = []
        for idx, hit in enumerate(hits):
            source = hit["_source"]
            # The raw pack string and pack id (not database id)
            raw_pack_str: str = source["pack_info"]
            pack_id: str = source["doc_id"]

            # Now you can write the pack into the database and generate url.
            item = {
                "name": f"clinical_results_{idx}",
                "textPack": raw_pack_str,
                "project_id": base_project_id,
            }

            db_id = sqlite_insert(conn, "stave_backend_document", item)
            answers += [db_id]
            print(pack_id, db_id)

        links: List[str] = create_links(config.Stave.url, answers)

        for link in links:
            st.write(link, unsafe_allow_html=True)

    if search:
        results = index_search(es, INDEX, search)
        hits = results["hits"]["hits"]

        conn = sqlite3.connect(config.Stave.stave_db_path)
        answers = []
        docs = []
        for idx, hit in enumerate(hits):
            source = hit["_source"]
            # The raw pack string and pack id (not database id)
            raw_pack_str: str = source["pack_info"]
            pack_id: str = source["doc_id"]
            highlight = "...".join(hit["highlight"]["content"])
            # Now you can write the pack into the database and generate url.
            item = {
                "name": f"clinical_results_{idx}",
                "textPack": raw_pack_str,
                "project_id": base_project_id,
            }

            db_id = sqlite_insert(conn, "stave_backend_document", item)
            answers += [db_id]

            docs.append(highlight)

        links: List[str] = create_links(config.Stave.url, answers)

        for i, _ in enumerate(links):
            st.write(links[i], unsafe_allow_html=True)
            st.write(
                templates.search_result(docs[i].replace("\n", " ")),
                unsafe_allow_html=True,
            )


if __name__ == '__main__':
    main()
