# forte-medical

## Installation
```shell
pip install -e .
```

## Medical Tasks
* blood_pressure_estimation
* chunking
* constituency_parsing
* context_analyzation
* coreference_resolution
* dependency_parsing
* icd_coding
* length_of_stay_prediction
* motality_prediction
* multivariate_time_series
* named_entity_recognition
* negation_context_analyzation
* pos_tagging
* status_context_analyzation
* temporal_relationships
* umls_entity_linking


## Usage
### Annotation
#### Command Line
```shell
./forte_medical_annotate \
    --text "xxx" (--file_to_annotate xxx) \
    --reader text_reader \
    --annotators pos_tagger,named_entity_recognizer,xxx
```

#### Python
```python
from forte import Pipeline
from forte_medical.readers import XMIReader
from forte_medical.annotators import POSTagger, NamedEntityRecognizer, ICDCoder

pipeline = Pipeline()
pipeline.set_reader(XMIReader())
pipeline.add(POSTagger(model='scispacy-en_core_sci_sm'))
pipeline.add(NamedEntityRecognizer(model=xxx))
pipeline.add(ICDCoder(model=xxx))
pipeline.run('Running SpaCy with Forte!')
```

### Training

#### Command Line
```shell
./forte_medical_train --data mimiciii (or a filepath) --task icd_coding
```

### Python
```python
from forte_medical.datasets import MIMICIII
from forte_medical.models import BERTClassifier
from forte_medical.trainers import ICDCodingTrainer

mimiciii = MIMICIII()
model = BERTClassifier()
trainer = ICDCodingTrainer()

trainer.fit(dataset=mimiciii, hparams=xxx)
```

## Package Structure
```
forte_medical/
├── annotate.py
├── evaluate.py
├── evaluators
│   ├── evaluator_base.py
│   ├── icd_coding_evaluator.py
│   └── ner_evaluator.py
├── models
│   ├── bert.py
│   └── model_base.py
├── ontology_specs
│   ├── icd_coding.json
│   ├── master.json
│   └── ner.json
├── processors
│   ├── chunker.py
│   ├── constituency_parser.py
│   ├── context_detector.py
│   ├── coreference_annotator.py
│   ├── dependency_parser.py
│   ├── icd_coder.py
│   ├── named_entity_recognizer.py
│   ├── pos_tagger.py
│   ├── temporal_relation_annotator.py
│   └── umls_entity_linker.py
├── readers
│   ├── jdbc_reader.py
│   ├── mimic_iii.py
│   ├── reader_base.py
│   ├── text_reader.py
│   └── xmi_reader.py
├── trainers
│   ├── icd_coding_trainer.py
│   ├── ner_trainer.py
│   └── trainer_base.py
└── train.py
```