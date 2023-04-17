from setuptools import setup, find_packages
import os

setup(
    name="citroen_model",
    author="Daniel Diego Horcajuelo",
    author_email="dadiego91@gmail.com",
    version="0.0.1",
    packages=find_packages(),
    scripts=[
        os.path.join("citroen", "training", "processing"),
        os.path.join("citroen", "training", "train"),
    ],
    requires=["awswrangler", "pandas", "scikit-learn"],
)
