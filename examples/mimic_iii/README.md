## A Clinical Information Processing Example - Demo medical pipeline

This project shows how we can run a pipeline retrieving information from MIMIC3 discharge notes.
 
## Install extra dependencies

To install the latest code directly from source,

```bash
pip install git+https://git@github.com/asyml/forte-wrappers#egg=forte.elastic\&subdirectory=src/elastic
pip install git+https://git@github.com/asyml/forte-wrappers#egg=forte.spacy\&subdirectory=src/spacy
```

To install using ```pip```,
```bash
pip install forte.elastic
pip install forte.spacy
```

## Run demo
You can run the following command to parse some files like the MIMIC3 discharge notes.
```bash
python medical_pipeline.py /path/to/mimiciii/1.4/NOTEEVENTS.csv.gz /path_to_sample_output 1000 True
```

Tha last command line argument is ```use_mimic3_data```, it informs the script whether it should run the pipeline on MIMIC3 files located at ```/path/to/mimiciii/1.4/NOTEEVENTS.csv.gz``` (```True```) or just process a single pack using a single text file of discharge notes already present in the code (```False```). 
The path of the text file has to be provided to run the pipeline with ```use_mimic3_data``` as ```False```.

```bash
python medical_pipeline.py sample_data/ /path_to_sample_output 1000 False
```

Here, we also write out the raw data pack to `/path_to_sample_output`, and only
process the first 1000 notes. Remove the `1000` parameter to index all documents.

