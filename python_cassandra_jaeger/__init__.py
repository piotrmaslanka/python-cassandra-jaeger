import warnings

from cassandra.cluster import Session
from cassandra.query import SimpleStatement
from opentracing import Tracer, Format, tags
from satella.cassandra import wrap_future

from satella.coding.structures import Proxy
from satella.opentracing import trace_future

__version__ = '0.3'


def _query_to_string(query, arguments):
    if isinstance(arguments, dict):
        args_str = str(arguments)
    else:
        args_str = ', '.join(map(str, arguments))

    if len(args_str) > 100:
        args_str = f'{args_str[:100]}...'

    if isinstance(query, SimpleStatement):
        query_str = query.query_string
        if len(query_str) > 100:
            query_str = f'{query.query_string[:100]}...'
    else:
        query_str = str(query)
        if len(query_str) > 100:
            query_str = f'{query_str[:100]}...'

    return query_str, args_str


class SessionTracer(Proxy):
    __slots__ = 'session', 'tracer'

    def __init__(self, session: Session, tracer: Tracer):
        super().__init__(session)
        self.session = session
        self.tracer = tracer

    def execute(self, query, arguments=None, *args, **kwargs):
        return self.execute_async(query, arguments, *args, **kwargs).result()

    def execute_async(self, query, arguments=None, *args, **kwargs):
        span = self.tracer.active_span      #: type: Span
        is_sampled = False
        if span is not None:
            try:
                is_sampled = span.is_sampled()   # jaeger-client's spans have this property
            except AttributeError:
                warnings.warn('Unsupported tracing mechanism. Please file an issue at '
                              'https://github.com/piotrmaslanka/python-cassandra-jaeger/issues '
                              'with a description of what you are using for tracing.'
                              'Every Cassandra request will be assumed to have been traced, '
                              'which may negatively impact your performance', RuntimeWarning)
                is_sampled = True       # if you are using some other tracing mechanism

        if is_sampled:
            query_str, args_str = _query_to_string(query, arguments)

            span = self.tracer.start_span('Cassandra query',
                                          tags={
                                               tags.SPAN_KIND: tags.SPAN_KIND_RPC_CLIENT,
                                               tags.DATABASE_TYPE: 'cassandra',
                                               tags.DATABASE_STATEMENT: query_str,
                                               'db.arguments': args_str
                                          })

            custom_payload = kwargs.get('custom_payload', {})
            self.tracer.inject(span.context, Format.HTTP_HEADERS, custom_payload)
            for k, v in custom_payload.items():
                if isinstance(v, str):
                    custom_payload[k] = v.encode('utf8')
            kwargs.update(trace=True,
                          custom_payload=custom_payload)

        cass_fut = self.session.execute_async(query, arguments, *args, **kwargs)
        if is_sampled:
            trace_future(wrap_future(cass_fut), span)
        return cass_fut
