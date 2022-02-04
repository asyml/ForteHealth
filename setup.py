import sys
import setuptools


if sys.version_info < (3, 6):
    sys.exit('Python>=3.6 is required by forte-medical.')

setuptools.setup(
    name="forte-medical",
    version='0.0.0',
    url="https://github.com/asyml/forte-medical",
    description="Medical NLP pipelines.",
    long_description=open("README.md", "r", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    license='',

    packages=setuptools.find_packages(
        exclude=["scripts*", "examples*", "tests*"]
    ),
    install_requires=[
        'forte',
    ],
    entry_points={
        'console_scripts': [
            "forte-medical-train=forte_medical_cli.train:main",
            "forte-medical-process=forte_medical_cli.process:main",
            "forte-medical-evaluate=forte_medical_cli.evaluate:main",
        ]
    },
    include_package_data=True,
    python_requires='>=3.6'
)