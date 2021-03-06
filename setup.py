#!/usr/bin/env python
""" file: setup.py (xjson)
    author: Jess Robertson, CSIRO Earth Science and Resource Engineering
    date: Wednesday 1 May, 2013

    description: Setuptools installer script for xjson.
"""

from setuptools import setup, find_packages
import os

def read(*paths):
    """ Build a file path from *paths and return the contents.
    """
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

# Get requirements from requirements.txt file
with open('requirements.txt') as fhandle:
    REQUIREMENTS = [l.strip('\n') for l in fhandle]

# Get version number from _version.py
# Can be updated using python setup.py update_version
from update_version import update_version, Version, get_version
update_version()

## PACKAGE INFORMATION
setup(
    # XJson
    name='xjson',
    version=get_version(),
    description='XML and JSON, without the heartbutn',
    long_description='making something good here',
    author='Jess Robertson',
    author_email='jesse.robertson@csiro.au',
    url='http://github.com/jesserobertson/xjson',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2 :: Only',
        'Topic :: Internet',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: XML'
    ],

    # Dependencies
    install_requires=REQUIREMENTS,

    # Contents
    packages=find_packages(exclude=['test*']),
    package_data={
        'xjson.xjson': ['*.json'],
    },
    test_suite='tests',
    cmdclass={
        'update_version': Version
    }
)
