## A Clinical Information Processing Example

This example shows how we can construct a project to make ForteHealth and Stave work side by side.

## Install extra dependencies

To install the latest code directly from source,

```bash
pip install git+https://git@github.com/asyml/forte-wrappers#egg=forte.elastic\&subdirectory=src/elastic
pip install git+https://git@github.com/asyml/forte-wrappers#egg=forte.spacy\&subdirectory=src/spacy
pip install git+https://git@github.com/asyml/forte-wrappers#egg=forte.spacy\&subdirectory=src/nltk
pip install git+https://github.com/asyml/ForteHealth.git
pip install git+https://github.com/astml/stave.git
```

To install from PyPI,
```bash
pip install forte.elastic
pip install forte.spacy
pip install forte.nltk
pip install forte.health
pip install stave
```

## Downloading the models

This example includes the following six functions:
1. Sentence Segementation
2. Tokenization
3. Pos Tag
4. Bio Named Entity Recognition
5. Nagation Context Analysis
6. ICD Coding Detection

Before running the pipeline, we need to download the some of the models

```bash
python ./download_models.py 
```

**Note**: The above script will save the model in `resources/NCBI-disease`. Use `--path` option to save the model into a different directory.

## Set up the configuration
Before run Elastic Searcher and Stave, we need to ensure that the current configuration is compatible with the environment of our computer.

Please check and change the following configurations in `clinical_config.yml`:

1. Ensure `LastUtteranceSearcher.stave_db_path`(line 16) is the correct path -> `$Home/.stave`, e.g.,  `"/home/name/.stave"`
2. Ensure `Stave.username`(line 26) and `Stave.pw`(line 27) is `"admin"` and `"admin"`.




## Prepare elastic searcher
Download corresponding elasticsearch archive from https://www.elastic.co/downloads/past-releases/elasticsearch-7-17-2, unzip it and run `elasticsearch-7-17-2/bin/elasticsearch` to start the service. 

Run the following to check if elasticsearch is running properly:
```bash
curl -XGET localhost:9200/_cluster/health?pretty
```

Make sure you create index 'elastic_indexer' in the cluster before working with this example, you can run the following command:
```bash
curl -X PUT localhost:9200/elastic_indexer
```

You can also follow the online blog for more information:

https://www.elastic.co/guide/en/elasticsearch/reference/current/starting-elasticsearch.html


## Run indexer and Stave
First, you should start an Elastic Indexer backend.

Then, to start the Stave server that our pipeline will connect to for visualization purposes, run
```bash
stave -s start -o -l -n 8899
```

Here, you need to make sure `LastUtteranceSearcher.url` and `Stave.url` in `clinical_config.yml` are both `"http://localhost:8899"`. Or you can change the port 8899 to any port you like.


## Run demo pipeline

Now, open a new terminal, other than the one running stave server. You can run the following command to parse some files and index them.
```bash
python clinical_processing_pipeline.py path_to_mimiciii/1.4/NOTEEVENTS.csv.gz path_to_mimiciii_output 100 1
```

The last argument, `use_mimiciii_reader` is whether to use the `Mimic3DischargeNoteReader()`. If you set the argument to `1`, you will need to make sure the input data is mimic iii dataset, else `0` for `PlainTextReader()`.

If you do not have the mimic iii datasets and just want to test the function, you can run the following command to test the function with the given sample data:

```bash
python clinical_processing_pipeline.py sample_data/ path_to_sample_output/ -1 0
```

If we just need to check the remote pipeline connection to Stave. 

You can mask out Line 76 to Line 118 in `clinical_processing_pipeline.py`.

Hence, if you just wish to run the demo pipeline with existing database entries, and wish to just connect with Stave for visualization, You can mask out Line 74 to Line 118 in `clinical_processing_pipeline.py` and run this command:

```bash
python clinical_processing_pipeline.py ./ ./ 100 0
```

Here, we also write out the raw data pack to `/path_to_sample_output`, and only
index the first 100 notes. Remove the `100` parameter to index all documents.

## Visualization

You can go ahead and open `http://localhost:8899` on your browser to access Stave UI.
Next, you will see 2 projects, named as `clinical_pipeline_base` and `clinical_pipeline_chat` by default.

<img width="1437" alt="image" src="https://user-images.githubusercontent.com/14886942/174163073-d9c86f57-76c9-46f4-ade0-c0a81d7d71a6.png">

Click on `clinical_pipeline_chat` and then the document that resides within to go to the chatbot/search UI. Enter the keywords you want to search for in the elasticsearch indices. The pipeline would then return a bunch of documents that match your keywords. Click on those document links to access the Annotation Viewer UI for those documents.

<img width="1437" alt="image" src="https://user-images.githubusercontent.com/14886942/174163371-f6e56a25-7b51-48d9-969a-f8d7140c8c89.png">

<img width="1431" alt="image" src="https://user-images.githubusercontent.com/14886942/174163438-eef1c877-38f5-43e8-b792-9de33a467b33.png">


## Add the output data 
We write out the raw data pack to  `/path_to_sample_output`, so you can see many json files in the directory.

Click on `clinical_pipeline_base` and add the json file to the documents. Click on those document links to access the Annotation Viewer UI for those documents.