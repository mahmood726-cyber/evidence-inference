from setuptools import setup, find_packages

setup(
    name="evidence_inference",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "nltk",
        "scikit-learn",
        "torch",
        "pandas",
        "dill",
        "gensim",
        "scipy",
        "numpy",
        "ftfy",
        "pattern",
        "lxml",
        "spacy",
        "transformers", 
        "dacite"
    ],
)
