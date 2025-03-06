from unfazed.cache import caches
from unfazed.http import HttpRequest, HttpResponse

from .models import User


async def get_users(request: HttpRequest) -> HttpResponse:
    users = await User.all()
    return HttpResponse(f"get {len(users)} users")


async def create_user(request: HttpRequest) -> HttpResponse:
    user = User(name="test", email="test@test.com", password="test")
    await user.save()
    return HttpResponse(f"created user {user.id}")


async def bulk_create_users(request: HttpRequest) -> HttpResponse:
    users = [
        User(name=f"test-{i}", email=f"test-{i}@test.com", password=f"test-{i}")
        for i in range(10)
    ]
    await User.bulk_create(users)
    return HttpResponse(f"created {len(users)} users")


async def cache_get(request: HttpRequest) -> HttpResponse:
    cache = caches["default"]

    value = await cache.get("test")
    return HttpResponse(f"get {value}")


async def cache_set(request: HttpRequest) -> HttpResponse:
    cache = caches["default"]

    await cache.set("test", "test")
    return HttpResponse("successfully")
