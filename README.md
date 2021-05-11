# python-cassandra-jaeger
[![PyPI](https://img.shields.io/pypi/pyversions/python-cassandra-jaeger.svg)](https://pypi.python.org/pypi/python-cassandra-jaeger)
[![PyPI version](https://badge.fury.io/py/python-cassandra-jaeger.svg)](https://badge.fury.io/py/python-cassandra-jaeger)
[![PyPI](https://img.shields.io/pypi/implementation/python-cassandra-jaeger.svg)](https://pypi.python.org/pypi/python-cassandra-jaeger)

## When do I use it?

When I'm using the following technologies:

* [cassandra-driver](https://pypi.org/project/cassandra-driver/)
* [cassandra-jaeger-tracing](https://github.com/smok-serwis/cassandra-jaeger-tracing)

And you want to attach your traces to Cassandra's requests.

**Note: so far only Jaeger tracing is supported. I mean,** 
**theoretically every opentracing-compatible framework** 
**is supported, but only Jaeger's tracing enables to select**
**which query to trace or not.**

**In case that you're not using Jaeger, every single query will be**
**sent with a tracing request, which may negatively impact your**
**performance, Cassandra-wise.**

If you have an issue with that, please file an 
[issue](https://github.com/piotrmaslanka/python-cassandra-jaeger/issues)
with a description of what it is that you're using for tracing.

A relevant warning will be shown as well.

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

Just remember to match your tracing key with
Cassandra's `JAEGER_TRACE_KEY`.

## What does it do?

It hijacks `session.execute`, grabs the current span,
determines if sampling is active for this span (currently
works only with Jaeger) and if it is so, starts a new 
child span, attaches it's ID to custom_payload and enables
tracing for the request.

# Additionally metricizing your queries

*Added in v0.4*: 
You can also metrify how long did your queries take to execute, say:

```python
from satella.instrumentation.metrics import getMetric

met_sum = getMetric('cassandra.query.time.summary', 'summary')
s = c.connect('keyspace')
st = SessionTracer(s, tracer, metric=met_sum)
```

# History

## v0.4

* added an option to metricize the queries

## v0.3

* a warning will be shown with unsupported tracing mechanism

## v0.2
 
* improved reporting when arguments is a dict

