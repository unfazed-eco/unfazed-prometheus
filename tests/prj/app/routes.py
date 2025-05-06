import typing as t

from unfazed.route import Route, path

from .endpoints import (
    bulk_create_users,
    create_user,
    default_cache_get,
    default_cache_set,
    get_users,
    namespace_cache_get,
    namespace_cache_set,
    serializer_cache_get,
    serializer_cache_set,
)

patterns: t.List[Route] = [
    path("/user-list", endpoint=get_users),
    path("/user-create", endpoint=create_user),
    path("/user-bulk-create", endpoint=bulk_create_users),
    path("/default-cache-get", endpoint=default_cache_get),
    path("/default-cache-set", endpoint=default_cache_set),
    path("/namespace-cache-get", endpoint=namespace_cache_get),
    path("/namespace-cache-set", endpoint=namespace_cache_set),
    path("/serializer-cache-get", endpoint=serializer_cache_get),
    path("/serializer-cache-set", endpoint=serializer_cache_set),
]
