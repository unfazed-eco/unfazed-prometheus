import typing as t

from unfazed.route import Route, path

from .endpoints import (
    bulk_create_users,
    cache_get,
    cache_set,
    create_user,
    get_users,
)

patterns: t.List[Route] = [
    path("/user-list", endpoint=get_users),
    path("/user-create", endpoint=create_user),
    path("/user-bulk-create", endpoint=bulk_create_users),
    path("/cache-get", endpoint=cache_get),
    path("/cache-set", endpoint=cache_set),
]
