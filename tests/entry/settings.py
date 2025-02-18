import socket

UNFAZED_SETTINGS = {
    "MIDDLEWARES": [
        "unfazed_prometheus.middleware.common.PrometheusMiddleware",
    ],
    "LIFESPAN": ["unfazed_prometheus.lifespan.PrometheusLifespan"],
    "ROOT_URLCONF": "entry.routes",
}


PROMETHEUS_SETTINGS = {
    "HOSTNAME": socket.gethostname(),
    "PROJECT": "unfazed_prometheus",
    "CLIENT_CLASS": "unfazed_prometheus.settings.PrometheusSettings",
}
