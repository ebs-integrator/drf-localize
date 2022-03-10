import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

setup(
    name="drf-localize",
    version="0.0.1",
    author="Dorin Musteața",
    description="drf-localize is a package that provides mobile and API clients with localization experiences.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ebs-integrator/drf-localize",
    project_urls={
        "Bug Tracker": "https://github.com/ebs-integrator/drf-localize/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
)
