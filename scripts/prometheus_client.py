from prometheus_client import CollectorRegistry, make_asgi_app, multiprocess


def app(scope, receive, send):
    registry = CollectorRegistry()

    multiprocess.MultiProcessCollector(registry)

    return make_asgi_app(registry)
