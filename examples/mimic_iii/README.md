## A Clinical Information Processing Example - Demo medical pipeline

This project shows how we can run a pipeline retrieving information from MIMIC3 discharge notes.
 
## Install extra dependencies

In command line, we run

```bash
pip install git+https://git@github.com/asyml/forte-wrappers#egg=forte-wrappers[elastic,spacy]
```

## Run indexer
First, you should start an Elastic Indexer backend.

Second, you can run the following command to parse some files and index them.
```bash
python medical_pipeline.py /path/to/mimiciii/1.4/NOTEEVENTS.csv.gz /path_to_sample_output 1000 False
```

Tha last command line argument is ```singlePack```, it informs the script whether it should run the pipeline on MIMIC3 files located at '/path/to/mimiciii/1.4/NOTEEVENTS.csv.gz' (```False```) or just process a single pack using a single string of discharge note already present in the code (```True```).

Here, we also write out the raw data pack to `/path_to_sample_output`, and only
index the first 1k notes. Remove the `1000` parameter to index all documents.

After the indexing is done, we are ready with the data processing part. Let's start the GUI.

## Stave 
First, set up Stave following the instructions.

Second, create an empty project with the [default ontology](https://github.com/asyml/forte/blob/master/forte/ontology_specs/base_ontology.json),
 now record the project id.

Set up the following environment variables:
```bash
export stave_db_path=[path_to_stave]/simple_backend/db.sqlite3
export url_stub=http://localhost:3000
export query_result_project_id=[the project id above]
```

Now, create another project with default ontology.

Upload the `*.json` file (you can find it in the directory of the README) to the project.

