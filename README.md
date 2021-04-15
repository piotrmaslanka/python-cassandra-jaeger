# python-cassandra-jaeger
[![PyPI](https://img.shields.io/pypi/pyversions/python-cassandra-jaeger.svg)](https://pypi.python.org/pypi/python-cassandra-jaeger)
[![PyPI version](https://badge.fury.io/py/python-cassandra-jaeger.svg)](https://badge.fury.io/py/python-cassandra-jaeger)
[![PyPI](https://img.shields.io/pypi/implementation/python-cassandra-jaeger.svg)](https://pypi.python.org/pypi/python-cassandra-jaeger)


## When do I use it?

When I'm using the following technologies:

* [cassandra-driver](https://pypi.org/project/cassandra-driver/)
* [cassandra-jaeger-tracing](https://github.com/smok-serwis/cassandra-jaeger-tracing)

And you want to attach your traces to Cassandra's requests.

## Usage

Just do the following:

```python
from python_cassandra_jaeger import SessionTracer
from cassandra.cluster import Cluster

from .tracing import tracer

c = Cluster(['127.0.0.1'])
s = c.connect('keyspace')
st = SessionTracer(s, tracer)

st.execute('SELECT * FROM table')
```

And you keep on utilizing `st` instead of `s`.
This will automatically execute tracing when your span is being traced.


For tracing cassandra-driver using smok-serwis/cassandra-jaeger-tracing
