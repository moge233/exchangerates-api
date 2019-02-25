#!/usr/bin/env python3


'''
setup.py

Setup file for the exchangeratesapi package
'''


import os
from setuptools import setup, find_packages


_DESCRIPTION = 'A package which provides a wrapper for the \
               exchangeratesapi.io API.'


def _readme():
    readme_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(readme_dir, 'README.md')) as readme:
        return readme.read()


setup(
        name='exchangeratesapi',
        version='0.0',
        description=_DESCRIPTION,
        long_description=_readme(),
        author='moge233',
        packages=find_packages(),
        test_suite='tests',
        include_package_data=True,
        zip_safe=False,
)
