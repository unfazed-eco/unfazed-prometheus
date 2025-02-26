import socket

UNFAZED_SETTINGS = {
    "MIDDLEWARE": [
        "unfazed_prometheus.middleware.common.PrometheusHttpRequestMiddleware",
    ],
    "LIFESPAN": ["unfazed_prometheus.lifespan.PrometheusLifespan"],
    "ROOT_URLCONF": "entry.routes",
}


UNFAZED_PROMETHEUS_SETTINGS = {
    "HOSTNAME": socket.gethostname(),
    "PROJECT": "unfazed_prometheus",
    "CLIENT_CLASS": "unfazed_prometheus.settings.PrometheusSettings",
    "PROMETHEUS_MULTIPROC_DIR": "/prometheus",
}
