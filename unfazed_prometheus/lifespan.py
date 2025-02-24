from unfazed.lifespan import BaseLifeSpan

from .base import agent


class PrometheusLifespan(BaseLifeSpan):
    async def on_startup(self) -> None:
        try:
            agent.setup()
        except Exception as e:
            raise RuntimeError("prometheus setup failed") from e
