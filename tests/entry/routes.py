from unfazed.http import HttpRequest, HttpResponse
from unfazed.route import path


async def hello1(request: HttpRequest) -> HttpResponse:
    return HttpResponse("hello1")


async def hello2(request: HttpRequest) -> HttpResponse:
    return HttpResponse("hello2")


patterns = [
    path("/api/hello1", endpoint=hello1),
    path("/api/hello2", endpoint=hello2),
]
