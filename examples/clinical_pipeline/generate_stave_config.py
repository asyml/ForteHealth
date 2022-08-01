import json
from forte import ontology_specs


def get_json(path: str):
    file_obj = open(path)
    data = json.load(file_obj)
    file_obj.close()
    return data


def main():
    clinical_ontology = get_json("clinical_pipeline_ontology.json")
    base_ontology = get_json(
        ontology_specs.__path__[0] + "//base_ontology.json"
    )

    merged_ontology = dict()
    merged_ontology["name"] = "clinical_ontology"
    merged_ontology["definitions"] = (
        base_ontology["definitions"] + clinical_ontology["definitions"]
    )

    default_onto_project = dict()
    default_onto_project["name"] = "clinical_pipeline_base"
    default_onto_project["project_type"] = "single_pack"
    default_onto_project["ontology"] = merged_ontology
    default_onto_project["config"] = get_json("stave_onto_config.json")

    with open("defualt_onto_project.json", "w") as fp:
        json.dump(default_onto_project, fp)

    chat_project = dict()
    chat_project["name"] = "chat_project"
    chat_project["project_type"] = "single_pack"
    chat_project["ontology"] = merged_ontology
    chat_project["config"] = get_json("stave_chat_config.json")

    with open("chat_project.json", "w") as fp:
        json.dump(chat_project, fp)


if __name__ == "__main__":
    main()
