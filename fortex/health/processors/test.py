import spacy
from timexy import Timexy

nlp = spacy.load("en_core_web_sm")

# Optionally add config if varying from default values
config = {
    "kb_id_type": "timex3",  # possible values: 'timex3'(default), 'timestamp'
    "label": "timexy",  # default: 'timexy'
    "overwrite": False,  # default: False
}
nlp.add_pipe("timexy", config=config, before="ner")

doc = nlp(
    "Today is the 10.10.2010. I was in Paris for six years. 2 pm 3 days ago"
)
for e in doc.ents:
    print(f"{e.text}\t{e.label_}\t{e.kb_id_}")
