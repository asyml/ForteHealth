## A search engine example using Streamlit

This example shows how we use ForteHealth pipelines to build processors to process mimic III dataset and show the results through streamlit

## Install extra dependencies

To install from PyPI,
```bash
pip install forte
pip install forte.elastic
pip install forte.spacy
pip install forte.huggingface
pip unstall forte.nltk
pip install forte.health
pip install streamlit
pip install spacy_streamlit
```

## Downloading the models

Before running the pipeline, we need to download the some of the models

```bash
python ./download_models.py 
```

**Note**: The above script will save the model in `resources/NCBI-disease`. Use `--path` option to save the model into a different directory.

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

## Run pipeline
First, you should start an Elastic Indexer backend.

Now, open a terminal. You can run the following command to parse some files and index them.
```bash
python clinical_processing_pipeline.py path_to_mimiciii/1.4/NOTEEVENTS.csv.gz path_to_mimiciii_output 10
```

Here, we write out the raw data pack to `/path_to_sample_output`, and only index the first 10 notes. You can change the number to whatever you want in the above command.

Also, we write the data into elasticsearch. You can run the command line to check whether the 10 notes are written into your database:

```bash
curl -X GET localhost:9200/elastic_indexer/_search
```
## Run streamlit

Make sure the Elasticsearch server is started and the python version should be >= 3.7.2. (to run streamlit)

Now, open the terminal. Run the following command to start the streamlit.
```bash
streamlit run mutiple_pages.py
```

Now open  `http://localhost:8501` on your browser to access the streamlit interface.

Next, you will see the ten reports shown on the middle of the website, and on the right, you will see the content of the reports and the disease named entities are annotated.



<img width="1437" alt="image" src="https://raw.githubusercontent.com/Leolty/ImageRepository/main/Forte/1658069753890.jpg">



You can also search in the input text, for example, if you search "*Cancer*", the reports including "*Cancer*" will be shown.

Change the functions in the sidebar to *Plain Text Input*, you will see this:

<img width="1437" alt="image" src="https://raw.githubusercontent.com/Leolty/ImageRepository/main/Forte/1658071440722.png">



You can input whatever you want, and this realize the function of some basic Named Entity Recognition (for example, Date, Person or Organization). 
