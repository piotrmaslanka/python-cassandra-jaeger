#!/usr/bin/env python

from distutils.core import setup

from setuptools import find_packages

import python_cassandra_jaeger


setup(version=python_cassandra_jaeger.__version__,
      packages=find_packages(include=['python_cassandra_jaeger']),
      )
