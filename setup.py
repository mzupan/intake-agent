#!/usr/bin/env python

from setuptools import setup, find_packages

files = ["intake/*"]

setup(
    name = 'intake-agent',
    version = "0.1",
    description = "The InTake agent that handles all the log sending",
    author = "Mike Zupan",
    author_email = "mike@zcentric.com",
    packages = find_packages(),
    entry_points={
        'console_scripts': [
            'intake-agent = intake.main:main',
        ]
    },
)
