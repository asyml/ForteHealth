import sys
from pathlib import Path
import setuptools
import subprocess
import os


long_description = (Path(__file__).parent / "README.md").read_text()

if sys.version_info < (3, 6):
    sys.exit("Python>=3.6 is required by forte-medical.")

# If we install neuralcoref and spacy at the same
# time, neuralcoref will throw "Cython failed" during building,
# which is because neuralcoref does not set them as dependencies
# properly.
# Therefore, we must install neuralcoref after cython and spacy
# are installed.
p = subprocess.call(
    [
        sys.executable,
        "-m",
        "pip",
        "install",
        "forte.spacy",  # TODO: version
        "cython>=0.25",
    ],
    env=os.environ,
)
if p != 0:
    raise RuntimeError("Installing NeuralCoref dependencies failed.")

setuptools.setup(
    name="forte.health",
    version="0.1.0",
    url="https://github.com/asyml/ForteHealth",
    description="NLP pipeline framework for biomedical and clinical domains",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache License Version 2.0",
    packages=setuptools.find_namespace_packages(
        include=["fortex.health", "ftx.*"], exclude=["scripts*", "examples*", "tests*"]
    ),
    namespace_packages=["fortex"],
    install_requires=[
        "forte~=0.2.0",
        "mypy_extensions==0.4.3",
        "texar-pytorch",
        "fastapi==0.65.2",
        "uvicorn==0.14.0",
        "forte.spacy",  # TODO: version
        "cython>=0.25",
    ],
    extras_require={
        "test": [
            "ddt",
            "testfixtures",
            "transformers==4.2.2",
            "protobuf==3.19.4",
            "pytest",
            "neuralcoref @ git+https://git@github.com/huggingface/neuralcoref.git@4.0.0#egg=neuralcoref",
        ],
        "icd_coding": [
            "transformers",
        ],
        "coreference": [
            "neuralcoref @ git+https://git@github.com/huggingface/neuralcoref.git@4.0.0#egg=neuralcoref",
        ],
    },
    entry_points={
        "console_scripts": [
            "forte-medical-train=forte_medical_cli.train:main",
            "forte-medical-process=forte_medical_cli.process:main",
            "forte-medical-evaluate=forte_medical_cli.evaluate:main",
        ]
    },
    include_package_data=True,
    python_requires=">=3.6",
)
