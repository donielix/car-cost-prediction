from setuptools import setup, find_packages
import os

setup(
    name="citroen_model",
    author="Daniel Diego Horcajuelo",
    author_email="dadiego91@gmail.com",
    version="0.0.1",
    packages=find_packages(),
    scripts=[
        os.path.join("citroen", "training", "processing.py"),
        os.path.join("citroen", "training", "train.py"),
        os.path.join("citroen", "pull.py"),
    ],
    install_requires=["awswrangler", "pandas", "scikit-learn"],
)
