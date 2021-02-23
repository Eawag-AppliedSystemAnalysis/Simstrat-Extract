# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Simstrat-Extract',
    version='0.1.0',
    description='Extra data from Simstrat output files for visualisation and web integration.',
    long_description=readme,
    author='James Runnalls',
    author_email='james.runnalls@eawag.ch',
    url='https://github.com/Eawag-AppliedSystemAnalysis/Simstrat-Extract',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)