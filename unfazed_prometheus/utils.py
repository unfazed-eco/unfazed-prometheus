import typing as t


def get_function_name(func: t.Callable, *args: t.Any, **kwargs: t.Any) -> str:
    return func.__name__
