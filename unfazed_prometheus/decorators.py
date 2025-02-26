import asyncio
import typing as t
from functools import wraps

from prometheus_client import Counter, Histogram

Label = t.Union[str, t.Callable[[t.Callable], str]]
Labels = t.List[Label]


def meta_monitor(
    counter_handler: t.Optional[Counter] = None,
    hist_handler: t.Optional[Histogram] = None,
    exc_handler: t.Optional[Counter] = None,
    counter_labels: t.Optional[Labels] = None,
    hist_labels: t.Optional[Labels] = None,
    exc_labels: t.Optional[Labels] = None,
) -> t.Callable:
    """
    Decorator to monitor the execution of a function.

    Args:
        inc_handler: Counter to increment when the function is called.
        hist_handler: Histogram to observe the execution time of the function.
        exc_handler: Counter to increment when the function raises an exception.

    Usage:
        @meta_monitor(
            inc_handler=RequestCounter,
            hist_handler=RequestDurationHistogram,
            exc_handler=ExceptionCounter,
        )
        def my_function(*args, **kwargs) -> t.Any:
            pass


    """

    def decorator(func: t.Callable) -> t.Callable:
        if counter_handler:
            new_counter_labels = counter_labels or []
            counter_str_labels = [
                label(func) if callable(label) else label
                for label in new_counter_labels
            ]
            counter_handler_target = counter_handler.labels(*counter_str_labels)
        else:
            counter_handler_target = None

        if hist_handler:
            new_hist_labels = hist_labels or []
            hist_str_labels = [
                label(func) if callable(label) else label for label in new_hist_labels
            ]
            hist_handler_target = hist_handler.labels(*hist_str_labels)
        else:
            hist_handler_target = None

        if exc_handler:
            new_exc_labels = exc_labels or []
            exc_str_labels = [
                label(func) if callable(label) else label for label in new_exc_labels
            ]
            exc_handler_target = exc_handler.labels(*exc_str_labels)
        else:
            exc_handler_target = None

        def counter_inc():
            if counter_handler_target:
                counter_handler_target.inc()

        def exc_inc():
            if exc_handler_target:
                exc_handler_target.inc()

        @wraps(func)
        async def wrapper(*args: t.Any, **kwargs: t.Any) -> t.Any:
            counter_inc()

            async def _wrapper():
                try:
                    return await func(*args, **kwargs)
                except Exception as err:
                    exc_inc()
                    raise err

            if hist_handler_target:
                with hist_handler_target.time():
                    return await _wrapper()
            else:
                return await _wrapper()

        @wraps(func)
        def sync_wrapper(*args: t.Any, **kwargs: t.Any) -> t.Any:
            counter_inc()

            def _wrapper():
                try:
                    return func(*args, **kwargs)
                except Exception as err:
                    exc_inc()
                    raise err

            if hist_handler_target:
                with hist_handler_target.time():
                    return _wrapper()
            else:
                return _wrapper()

        return wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return decorator
