from unfazed.lifespan import BaseLifeSpan

from .base import agent


class PrometheusLifespan(BaseLifeSpan):
    async def on_startup(self) -> None:
        print("prometheus on_startup")
        agent.setup()
