#!/usr/bin/env python

from setuptools import setup, find_packages

files = ["gitsync/*"]

setup(
    name = 'InTake',
    version = "0.1",
    description = "The InTake agent that handles all the log sending",
    author = "Mike Zupan",
    author_email = "mzupan@shopopensky.com",
    packages = find_packages(),
    entry_points={
        'console_scripts': [
            'intake = intake.main:main',
        ]
    },
)