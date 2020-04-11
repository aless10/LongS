#!/usr/bin/env python
import os

from setuptools import setup
from pkg_resources import parse_requirements

req_file = os.path.join(os.path.dirname(__file__), "requirements.txt")

with open(req_file, "r") as inst_reqs:
    install_requires = [str(req) for req in parse_requirements(inst_reqs)]

setup(
    name="LongS Checkouter",
    version="0.1.0.dev",
    author="Me",
    description="",
    packages=[],
    entry_points='''
    [console_scripts]
        esselunga=main:main
    ''',
    include_package_data=True,
    classifiers=[
        "Development Status :: 1 - Beta",
        "Programming Language :: Python",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: System :: Software Distribution",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
