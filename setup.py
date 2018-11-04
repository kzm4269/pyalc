#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='pyalc',
    version='0.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'lxml',
    ],
    entry_points={
        'console_scripts': [
            'alc = alc.interpreter:run',
        ],
    }
)
