import sys
from pathlib import Path
import setuptools


long_description = (Path(__file__).parent / "README.md").read_text()

if sys.version_info < (3, 6):
    sys.exit('Python>=3.6 is required by forte-medical.')

setuptools.setup(
    name="forte.health",
    version='0.1.0',
    url="https://github.com/asyml/ForteHealth",
    description="NLP pipeline framework for biomedical and clinical domains",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Apache License Version 2.0',
    packages=setuptools.find_namespace_packages(
        include=['fortex.health', 'ftx.*'],
        exclude=["scripts*", "examples*", "tests*"]
    ),
    namespace_packages=["fortex"],
    install_requires=[
        'forte~=0.2.0',
    ],
    extras_require={
        "test": [
            "ddt",
            "testfixtures",
            "transformers==4.18.0",
            "protobuf==3.19.4",
            "Pillow==8.4.0",
        ],
        "scispacy_processor": [
            "scispacy==0.5.0",
            "en-core-sci-sm @ https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.0/en_core_sci_sm-0.5.0.tar.gz"
        ],
    },
    include_package_data=True,
    python_requires='>=3.6',
)
