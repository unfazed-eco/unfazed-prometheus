import os
import socket

UNFAZED_SETTINGS = {
    "MIDDLEWARE": [
        "unfazed_prometheus.middleware.common.PrometheusHttpRequestMiddleware",
    ],
    "LIFESPAN": ["unfazed_prometheus.lifespan.PrometheusLifespan"],
    "ROOT_URLCONF": "entry.routes",
    "DATABASE": {
        "CONNECTIONS": {
            "default": {
                "ENGINE": "unfazed_prometheus.database.tortoise.mysql",
                "CREDENTIALS": {
                    "HOST": os.getenv("MYSQL_HOST", "mysql"),
                    "PORT": 3306,
                    "USER": "app",
                    "PASSWORD": "app",
                    "DATABASE": "app",
                },
            }
        },
    },
    "CACHE": {
        "default": {
            "BACKEND": "unfazed_prometheus.cache.backends.default.PrometheusDefaultBackend",
            "LOCATION": os.getenv("REDIS_URL", "redis://redis:6379"),
            "OPTIONS": {
                "decode_responses": True,
                "max_connections": 1000,
            },
        }
    },
    "INSTALLED_APPS": ["app"],
}


UNFAZED_PROMETHEUS_SETTINGS = {
    "HOSTNAME": socket.gethostname(),
    "PROJECT": "unfazed_prometheus",
    "CLIENT_CLASS": "unfazed_prometheus.settings.PrometheusSettings",
    "PROMETHEUS_MULTIPROC_DIR": os.getenv("PROMETHEUS_MULTIPROC_DIR", "/prometheus"),
}
