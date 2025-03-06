from starlette.types import ASGIApp, Receive, Scope, Send

from unfazed_prometheus.base import agent


class PrometheusHttpRequestMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app
        self.agent = agent

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        @self.agent.monitor_request(scope)
        async def call_wrapper() -> None:
            await self.app(scope, receive, send)

        await call_wrapper()
