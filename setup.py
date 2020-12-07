#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
import sys
#import setuptools
import subprocess
from setuptools import setup
from setuptools import find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools.command.egg_info import egg_info
# def npm_install(args=["npm","--global", "install", "apify"]):
#     subprocess.Popen(args, shell=True)

def custom_command():
    import sys
    if sys.platform in ['darwin', 'linux']:
        print("\n\n***** Installing apify from npm ...", flush=True)
        node_folder_path = os.path.join(os.path.expanduser("~"), ".alternat")
        if not os.path.exists(node_folder_path):
            os.mkdir(node_folder_path)
        try:
            output = subprocess.check_output(["npm", "install", "apify"], cwd=node_folder_path)
            #print(output, file=sys.stderr)
        except subprocess.CalledProcessError as e:
            print("\n Subprocess error")
            sys.exit(str(e.output))
    else:
        print("skipping installation of apify, Please make sure to install pytorch first")


class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        custom_command()


class CustomDevelopCommand(develop):
    def run(self):
        develop.run(self)
        custom_command()


class CustomEggInfoCommand(egg_info):
    def run(self):
        egg_info.run(self)
        custom_command()


with open("Readme.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

#if sys.version_info >= (3,8):
#    sys.exit("Python version greater than 3.7 not supported because of numpy and moviepy compatibility issues with python version 3.8")



# helper functions to make it easier to list dependencies not as a python list, but vertically w/ optional built-in comments to why a certain version of the dependency is listed
def cleanup(x):
    return re.sub(r" *#.*", "", x.strip())  # comments


def to_list(buffer):
    return list(filter(None, map(cleanup, buffer.splitlines())))


# normal dependencies ###
#
# these get resolved and installed via either of these two:
#
#   pip install alternat
#   pip install -e .
#
# IMPORTANT: when updating these, please make sure to sync conda/meta.yaml
dep_groups = {
    "core": to_list(
        """
        pillow
        google-cloud-vision==1.0.0
        tldextract
        easyocr
        pyyaml
        treelib
        uvicorn
        fastapi==0.62.0
        typer==0.3.2
"""
    )
}

__version__ = None # Explicitly set version.
# TODO use os.path instead of front slash
exec(open('alternat/version.py').read()) # loads __version__

requirements = [y for x in dep_groups.values() for y in x]
setup_requirements = to_list(
    """
    pytest-runner
    setuptools>=36.2
"""
)


# test dependencies ###
test_requirements = to_list(
    """
    pytest
"""
)

#mkdir my-project
#cd my-project
#npm install bitcoinjs-lib

setup(
    name="alternat",
    version=__version__,
    author="keplerlab",
    author_email="keplerwaasi@gmail.com",
    description="Alternat is a tool that automates alt text generation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/keplerlab/alternat.git",
    packages=find_packages(),
    install_requires=requirements,
    setup_requires=setup_requirements,
    tests_require=test_requirements,
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Documentation": "https://alternat.readthedocs.io",
        "Source": "https://github.com/keplerlab/alternat",
        "Tracker": "https://github.com/keplerlab/alternat/issues",
    },
    cmdclass={
        'install': CustomInstallCommand,
        'develop': CustomDevelopCommand,
        'egg_info': CustomEggInfoCommand,
    },
    include_package_data=True,
    zip_safe=False,
)
