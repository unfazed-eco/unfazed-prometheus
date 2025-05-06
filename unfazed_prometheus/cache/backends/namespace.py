import typing as t

from unfazed_prometheus import agent

try:
    from unfazed_redis.backends.namespaceclient import NamespaceClient
except ImportError:  # pragma: no cover
    raise ImportError("unfazed-redis is not installed")  # pragma: no cover


class PrometheusNamespaceBackend(NamespaceClient):
    def __init__(
        self, location: str, options: t.Dict[str, t.Any] | None = None
    ) -> None:
        super().__init__(location, options)

        old_execute_command = self.client.execute_command
        new_execute_command = agent.monitor_cache(old_execute_command)
        self.client.execute_command = new_execute_command
