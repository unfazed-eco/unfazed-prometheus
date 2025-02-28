import typing as t

from unfazed.cache.backends.redis import DefaultBackend

from unfazed_prometheus import agent


class PrometheusDefaultBackend(DefaultBackend):
    @agent.monitor_cache
    def __getattr__(self, name: str) -> t.Any:
        return super().__getattr__(name)
