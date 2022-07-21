## NER Label Example

This example shows how we start a search engine in streamlit and link the search results to stave.

## Install extra dependencies

To install from PyPI,
```bash
pip install forte.elastic
pip install forte.health
pip install stave
pip install streamlit
```

## Download spaCy model

run the following command to download the model
```bash
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.0/en_ner_bc5cdr_md-0.5.0.tar.gz
```

## Set up the configuration
Before run Elastic Searcher and Stave, we need to ensure that the current configuration is compatible with the environment of our computer.

Please check and change the following configurations in `stave_config.yml`:

1. Ensure `Stave.stave_db_path` is the correct path -> `$Home/.stave`, e.g.,  `"/home/name/.stave"`.
2. Ensure `Stave.username` and `Stave.pw`is `"admin"` and `"admin"`.

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
python clinical__pipeline.py path_to_mimiciii/1.4/NOTEEVENTS.csv.gz path_to_mimiciii_output 10 1
```

Here, we write out the raw data pack to `/path_to_sample_output`, and only index the first 10 notes. You can change the number to whatever you want in the above command.

Also, we write the data into elasticsearch. You can run the command line to check whether the 10 notes are written into your database:

```bash
curl -X GET localhost:9200/elastic_indexer/_search
```

## Run indexer and Stave
Again, you should start an Elastic Indexer backend.

Then, to start the Stave server that our pipeline will connect to for visualization purposes, run
```bash
stave -s start -o -l -n 8899
```
Then, login with username (admin) and password (admin).

Here, you need to make sure `Stave.url` in `stave_config.yml` is `"http://localhost:8899"`. Or you can change the port 8899 to any port you like.

## Run streamlit

To run streamlit, the python version should be >= 3.7.2. 

Now, open the terminal. Run the following command to start the streamlit.
```bash
streamlit run search_engine.py
```

Now open  `http://localhost:8501` on your browser to access the streamlit interface.

Next, you will see the reports shown on the interface. You can also search with the search engine.

Click the report with link, it will link to Stave, the visualization and annotation page.

Click the radio (Disease and Chemical) on the sidebar,  you can see the annotations on the UI.
