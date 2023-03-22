

<p align="center">
   <a href="https://github.com/asyml/ForteHealth/actions/workflows/main.yml"><img src="https://github.com/asyml/ForteHealth/actions/workflows/main.yml/badge.svg" alt="build"></a>
      <a href="https://codecov.io/gh/asyml/ForteHealth"><img src="https://codecov.io/gh/asyml/ForteHealth/branch/master/graph/badge.svg" alt="test coverage"></a>
   <a href="https://github.com/asyml/ForteHealth/blob/master/LICENSE"><img src="https://img.shields.io/badge/license-Apache%202.0-blue.svg" alt="apache license"></a>
   <a href="https://gitter.im/asyml/community"><img src="http://img.shields.io/badge/gitter.im-asyml/forte-blue.svg" alt="gitter"></a>
   <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="code style: black"></a>
</p>

<p align="center">
  <a href="#installation">Download</a> •
  <a href="#quick-start-guide">Quick Start</a> •
  <a href="#contributing">Contribution Guide</a> •
  <a href="#license">License</a> •
  <a href="https://asyml-forte.readthedocs.io/en/latest">Documentation</a> •
  <a href="https://aclanthology.org/2020.emnlp-demos.26/">Publication</a>
</p>

-----------------
**ForteHealth is in the incubation stage and still under development**

**Bring good software engineering to your Biomedical/Clinical ML solutions, starting from Data!**

**ForteHealth** is a biomedical and clinical domain centric framework designed to engineer complex ML workflows for several tasks including, but not limited to, Medical Entity Recognition, Negation Context Analysis and ICD Coding. ForteHealth allows practitioners to build ML components in a composable and modular way. It works in conjunction with Forte and Forte-wrappers project, and leverages the tools defined there to execute general  tasks vital in the biomedical and clinical use cases. 

## Installation

To install from source:

```bash
git clone https://github.com/asyml/ForteHealth.git
cd ForteHealth
pip install .
```

To install some Forte adapter for some existing [libraries](https://github.com/asyml/forte-wrappers#libraries-and-tools-supported):

Install from PyPI:

```bash
pip install forte.health
```

Some tools are pre-requisites to a few tasks in our pipeline. For example, forte.spacy and stave maybe needed 
for a pipeline that implements NER with visualisation and so on, depending on the use case.
 ```bash
# To install other tools. Check here https://github.com/asyml/forte-wrappers#libraries-and-tools-supported for available tools.
pip install forte.spacy
pip install stave
```

Some components or modules in forte may require some [extra requirements](https://github.com/asyml/forte/blob/master/setup.py#L45):

Install ScispaCyProcessor:
```bash
pip install 'forte.health[scispacy_processor]'
```

Install TemporalNormalizingProcessor:
 ```bash
 pip install 'forte.health[normalizer_processor]'
 ```

## Quick Start Guide
Writing biomedical NLP pipelines with ForteHealth is easy. The following example creates a simple pipeline that analyzes the sentences, tokens, and medical named entities from a discharge note.

Before we start, make sure the SpaCy wrapper is installed. 
Also, make sure you have input text files in the ```input_path``` directory that are passed through to the processors.
```bash
pip install forte.spacy
```
Let's look at an example of a full fledged medical pipeline:

```python
from fortex.spacy import SpacyProcessor
from forte.data.data_pack import DataPack
from forte.data.readers import PlainTextReader
from forte.pipeline import Pipeline
from ft.onto.base_ontology import Sentence, EntityMention
from ftx.medical.clinical_ontology import NegationContext, MedicalEntityMention
from fortex.health.processors.negation_context_analyzer import (
    NegationContextAnalyzer,
)

pl = Pipeline[DataPack]()
pl.set_reader(PlainTextReader())
pl.add(SpacyProcessor(), config={
    "processors": ["sentence", "tokenize", "pos", "ner", "umls_link"],
    "medical_onto_type": "ftx.medical.clinical_ontology.MedicalEntityMention",
    "umls_onto_type": "ftx.medical.clinical_ontology.UMLSConceptLink",
    "lang": "en_ner_bc5cdr_md"
    })

pl.add(NegationContextAnalyzer())
pl.initialize()
```

Here we have successfully created a pipeline with a few components:
* a `PlainTextReader` that reads data from text files, given by the `input_path`
* a `SpacyProcessor` that calls SpaCy to split the sentences, create tokenization, 
  pos tagging, NER and umls_linking
* finally, the processor `NegationContextAnalyzer` detects negated contexts

Let's see it run in action!

```python
for pack in pl.process_dataset(input_path):
    for sentence in pack.get(Sentence):
        medical_entities = []
        for entity in pack.get(MedicalEntityMention, sentence):
            for ent in entity.umls_entities:
                medical_entities.append(ent)

        negation_contexts = [
             (negation_context.text, negation_context.polarity)
             for negation_context in pack.get(NegationContext, sentence)
        ]

	print("UMLS Entity Mentions detected:", medical_entities, "\n")
	print("Entity Negation Contexts:", negation_contexts, "\n")
```

We have successfully created a simple pipeline. In the nutshell, the `DataPack`s are
the standard packages "flowing" on the pipeline. They are created by the reader, and
then pass along the pipeline.

Each processor, such as our `SpacyProcessor` `NegationContextAnalyzer`,
interfaces directly with `DataPack`s and do not need to worry about the
other part of the pipeline, making the engineering process more modular. 

The above mentioned code snippet has been taken from the [Examples](https://github.com/asyml/ForteHealth/tree/master/examples/mimic_iii) folder.

To learn more about the details, check out of [documentation](https://asyml-forte.readthedocs.io/)!
The classes used in this guide can also be found in this repository or
[the Forte Wrappers repository](https://github.com/asyml/forte-wrappers/tree/main/src/spacy)

## And There's More
The data-centric abstraction of Forte opens the gate to many other opportunities.
Go to [this](https://github.com/asyml/forte#and-theres-more) link for more information

To learn more about these, you can visit:
* [Examples](https://github.com/asyml/ForteHealth/tree/master/examples)
* [Documentation](https://asyml-forte.readthedocs.io/)
* Currently we are working on some interesting [tutorials](https://asyml-forte.readthedocs.io/en/latest/index_toc.html), stay tuned for a full set of documentation on how to do NLP with Forte!


## Contributing
This project is part of the [CASL Open Source](http://casl-project.ai/) family.

If you are interested in making enhancement to Forte, please first go over our [Code of Conduct](https://github.com/asyml/ForteHealth/master/CODE_OF_CONDUCT.md) and [Contribution Guideline](https://github.com/asyml/ForteHealth/master/CONTRIBUTING.md)

## About

### Supported By

<p align="center">
   <img src="https://user-images.githubusercontent.com/28021889/165799232-2bb9f819-f394-4ade-98b0-c55c751ec8b1.png", width="180" align="top">
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
   <img src="https://user-images.githubusercontent.com/28021889/165799272-9e51b864-04f6-432a-92e8-e0f84e091f72.png" width="180" align="top">
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
   <img src="https://user-images.githubusercontent.com/28021889/165802470-f478de54-6c44-4ec8-8cab-ba74ed1f0163.png" width="180" align="top">
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
</p>

![image](https://user-images.githubusercontent.com/28021889/165806563-1542aeac-9656-4ad4-bf9c-f9a2e083f5d8.png)

### License

[Apache License 2.0](https://github.com/asyml/forte/blob/master/LICENSE)
