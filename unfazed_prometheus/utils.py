import typing as t


def get_function_name(func: t.Callable, *args: t.Any, **kwargs: t.Any) -> str:
    return func.__name__


def get_first_arg_name(func: t.Callable, *args: t.Any, **kwargs: t.Any) -> str:
    return args[1]


def get_first_arg_first_letter(func: t.Callable, *args: t.Any, **kwargs: t.Any) -> str:
    query = args[1]
    return query.split(" ")[0]
