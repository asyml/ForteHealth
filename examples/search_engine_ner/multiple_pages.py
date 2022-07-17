from __future__ import annotations
import streamlit as st
from elasticsearch import Elasticsearch
from search_utils import all_search, index_search
import templates
import spacy_streamlit
import json
from pipelines import process_data


st.set_page_config(page_title="ForteHealth_Search_Engine", layout="wide")

PAGES = ["Search Engine", "Plain Text Input"]
es = Elasticsearch(hosts=["http://localhost:9200/"])
INDEX = "elastic_indexer"

page = st.sidebar.selectbox("Functions:", PAGES)

# search engine
if page == PAGES[0]:
    r1c1, r1c2 = st.columns([6, 6])
    with r1c1:
        st.title("Search the MIMIC III Data...")
        search = st.text_input("Enter search words:")

        if not search:
            records = {}
            results = all_search(es, INDEX)
            for i in range(len(results["hits"]["hits"])):
                result = results["hits"]["hits"][i]
                res = result["_source"]
                annotations = json.loads(res["pack_info"])["py/state"]["annotations"]

                ents = []
                for annotation in annotations:
                    if "EntityMention" in annotation["py/object"]:
                        ents.append(
                            {
                                "start": annotation["py/state"]["_span"]["begin"],
                                "end": annotation["py/state"]["_span"]["end"],
                                "label": annotation["py/state"]["ner_type"],
                            }
                        )
                records[res["doc_id"]] = [res["content"], ents]

            options = []
            for key in records:
                options.append(key)

            if options:
                myradio = st.radio(
                    label="Select a report:",
                    options=options,
                    index=0,
                    format_func=lambda x: f"Report# {x}",
                    key="radio_demo",
                    help="Click the radio button please",
                )

                with r1c2:
                    data = [
                        {
                            "text": records[myradio][0],
                            "ents": records[myradio][1],
                            "title": None,
                        }
                    ]

                    spacy_streamlit.visualize_ner(
                        data,
                        labels=["DISEASE"],
                        show_table=False,
                        manual=True,
                        title="Disease NER Detection",
                    )
            else:
                st.warning("No results")

        if search:
            records = {}
            results = index_search(es, INDEX, search)
            total_hits = results["aggregations"]["match_count"]["value"]
            # show number of results and time taken
            st.write(
                templates.number_of_results(total_hits, results["took"] / 1000),
                unsafe_allow_html=True,
            )
            # search results
            for i in range(len(results["hits"]["hits"])):
                result = results["hits"]["hits"][i]
                res = result["_source"]
                annotations = json.loads(res["pack_info"])["py/state"]["annotations"]

                ents = []
                for annotation in annotations:
                    if "EntityMention" in annotation["py/object"]:
                        ents.append(
                            {
                                "start": annotation["py/state"]["_span"]["begin"],
                                "end": annotation["py/state"]["_span"]["end"],
                                "label": annotation["py/state"]["ner_type"],
                            }
                        )
                records[res["doc_id"]] = [res["content"], ents]

            options = []
            for key in records:
                options.append(key)

            if options:
                myradio = st.radio(
                    label="Select a report:",
                    options=options,
                    index=0,
                    format_func=lambda x: f"Report# {x}",
                    key="radio_demo",
                    help="Click the radio button please",
                )

                with r1c2:
                    data = [
                        {
                            "text": records[myradio][0],
                            "ents": records[myradio][1],
                            "title": None,
                        }
                    ]

                    spacy_streamlit.visualize_ner(
                        data,
                        labels=["DISEASE"],
                        show_table=False,
                        manual=True,
                        title="Disease NER Detection",
                    )
            else:
                st.warning("No results")


# Plain Text
if page == PAGES[1]:

    st.title("Named Entity Recognition Visualization")
    form = st.form("ner")
    text = form.text_area(
        "Input your text here:", value="The CEO of Tesla is Ellon Musk."
    )

    if form.form_submit_button("Visualize"):
        pass

    ents = process_data(text)

    doc = [
        {
            "text": text,
            "ents": ents,
            "title": None,
        }
    ]

    spacy_streamlit.visualize_ner(
        doc,
        labels=[
            "ORG",
            "DATE",
            "NORP",
            "ORDINAL",
            "CARDINAL",
            "PERSON",
            "PERSENT",
            "GPE",
            "QUANTITY",
            "LAW",
            "MONEY",
        ],
        show_table=False,
        title="NER",
        manual=True,
    )
