#!/usr/bin/env python

from distutils.core import setup

from setuptools import find_packages

import python_cassandra_jaeger


setup(name='python-cassandra-jaeger',
      keywords=['cassandra', 'cassandra-driver', 'jaeger', 'opentracing', 'query'],
      version=python_cassandra_jaeger.__version__,
      packages=find_packages(include=['python_cassandra_jaeger']),
      install_requires=['cassandra-driver', 'opentracing', 'satella'],
      python_requires='!=2.7.*,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',
      )
