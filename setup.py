from setuptools import setup, find_packages

setup(
    name="ragmodelv2",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.0.0",
        "numpy",
        "langchain>=0.1.0",
        "langchain-community>=0.0.10",
        "thefuzz>=0.19.0",
        "python-Levenshtein",
        "SQLAlchemy>=2.0.0",
        "sentence-transformers>=2.2.2",
        "huggingface-hub>=0.23.0",
        "python-dotenv>=1.0.0",
    ],
)
