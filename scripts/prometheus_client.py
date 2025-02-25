from prometheus_client import (
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    generate_latest,
    multiprocess,
)
from starlette.types import Receive, Scope, Send


async def app(scope: Scope, receive: Receive, send: Send) -> None:
    if scope["type"] != "http":
        await send({"type": "http.response.body", "body": b"Not Found"})
        return

    registry = CollectorRegistry()

    multiprocess.MultiProcessCollector(registry)
    data = generate_latest(registry)

    status = "200 OK"
    headers = [
        ("Content-Type", CONTENT_TYPE_LATEST),
        ("Content-Length", str(len(data))),
    ]

    payload = await receive()
    if payload.get("type") == "http.request":
        await send(
            {
                "type": "http.response.start",
                "status": int(status.split(" ")[0]),
                "headers": headers,
            }
        )
        await send({"type": "http.response.body", "body": data})
    else:
        await send({"type": "http.response.body", "body": b"Not Found"})
