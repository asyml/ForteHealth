## A search engine demo using streamlit and stave

This example shows how we start a search engine in streamlit and link the search results to stave.

## Install extra dependencies

To install from PyPI,
```bash
pip install forte.elastic
pip install forte.health
pip install stave
pip install streamlit
```

## Set up the configuration
Before run Elastic Searcher and Stave, we need to ensure that the current configuration is compatible with the environment of our computer.

Please check and change the following configurations in `stave_config.yml`:

1. Ensure `Stave.stave_db_path` is the correct path -> `$Home/.stave`, e.g.,  `"/home/name/.stave"`.
2. Ensure `Stave.username`(line 26) and `Stave.pw`(line 27) is `"admin"` and `"admin"`.

## Start the elastic server

Before starting the search engine, you should make sure that the elasticsearch server is started, and you have run some pipelines to add some mimic iii reports in your database.

If not, please refer to the example https://github.com/asyml/ForteHealth/tree/master/examples/clinical_pipeline or another example https://github.com/asyml/ForteHealth/tree/master/examples/search_engine_ner to add some reports in your elasticsearch indexer, and start the server.

## Run indexer and Stave
Again, you should start an Elastic Indexer backend.

Then, to start the Stave server that our pipeline will connect to for visualization purposes, run
```bash
stave -s start -o -l -n 8899
```

Here, you need to make sure `Stave.url` in `stave_config.yml` is `"http://localhost:8899"`. Or you can change the port 8899 to any port you like.

## Run streamlit

To run streamlit, the python version should be >= 3.7.2. 

Now, open the terminal. Run the following command to start the streamlit.
```bash
streamlit run search_engine.py
```

Now open  `http://localhost:8501` on your browser to access the streamlit interface.

Next, you will see the reports shown on the interface.

<img width="1437" alt="image" src="https://raw.githubusercontent.com/Leolty/ImageRepository/main/Forte/1658078759617.png">



Click the report with link, it will link to Stave.

<img width="1437" alt="image" src="https://raw.githubusercontent.com/Leolty/ImageRepository/main/Forte/1658078805484.png">

You can also search the words in every reports, and also click the report to the Stave. 

<img width="1437" alt="image" src="https://raw.githubusercontent.com/Leolty/ImageRepository/main/Forte/1658078847447.png">

