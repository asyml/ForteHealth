## A ICD Code Prediction Demo

This demo shows how we can build pipeline to predict ICD-10 codes for medical notes.

The [International Classification of Diseases (ICD)](https://www.cdc.gov/nchs/icd/index.htm) is the classification used to code and classify mortality data from death certificates. We treat the ICD code prediction as a sequence classification task. That is, given an medical note, the model output its ICD code.

A key component of this demo is `ICDCodingProcessor`, which is implemented based on huggingface pre-trained models. In this demo, we use [AkshatSurolia/ICD-10-Code-Prediction](https://huggingface.co/AkshatSurolia/ICD-10-Code-Prediction). You can use other pre-trained models by changing the `model_name` config.

## Install extra dependencies

We need to install `forte.spacy`.

To install the latest code directly from source,

```bash
pip install git+https://git@github.com/asyml/forte-wrappers#egg=forte.spacy\&subdirectory=src/spacy
```

To install from PyPI,
```bash
pip install forte.spacy
```

## Run demo
You can run the following command to parse some files like the MIMIC3 discharge notes.

```bash
python icd_coding.py input_path output_path max_packs use_mimic3_reader

# Examples: 

# Read from MIMIC3:
python icd_coding.py /path/to/mimiciii/1.4/NOTEEVENTS.csv.gz /path_to_sample_output 1000 True

# Read from sample_data:
python icd_coding.py sample_data/ /path_to_sample_output 1000 False
```

The meaning of arguments:

- `input_path`: the path of input. Set it to mimic3 data if `use_mimic3_reader`=`True`, else set it to the directory of input files.
- `output_path`: the path to save data packs.
- `max_packs`: the max number of notes to read from mimic3 dataset. Set it to -1 to read all.
- `use_mimic3_reader`: whether to read with `Mimic3DischargeNoteReader`. If `True`, the `input_path` should be the mimic3 data. If `False`, the `input_path` should be a directory and files under that directory will be read with `PlainTextReader`.
