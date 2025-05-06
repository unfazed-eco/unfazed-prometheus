import logging
import typing as t

from unfazed.cache.backends.redis import SerializerBackend

from unfazed_prometheus import agent

logger = logging.getLogger("unfazed")


class PrometheusSerializerBackend(SerializerBackend):
    def __init__(
        self, location: str, options: t.Dict[str, t.Any] | None = None
    ) -> None:
        super().__init__(location, options)

        old_execute_command = self.client.execute_command
        new_execute_command = agent.monitor_cache(old_execute_command)
        self.client.execute_command = new_execute_command
