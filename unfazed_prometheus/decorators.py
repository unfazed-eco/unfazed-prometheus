import asyncio
import typing as t
from functools import wraps

from prometheus_client import Counter, Histogram

Label = t.Union[str, t.Callable[[t.Callable], str]]
Labels = t.List[Label]

Decorator = t.Callable[[t.Callable], t.Callable]


def meta_monitor(
    counter_handler: t.Optional[Counter] = None,
    hist_handler: t.Optional[Histogram] = None,
    exc_handler: t.Optional[Counter] = None,
    counter_labels: t.Optional[Labels] = None,
    hist_labels: t.Optional[Labels] = None,
    exc_labels: t.Optional[Labels] = None,
) -> Decorator:
    """
    Decorator to monitor the execution of a function.

    Args:
        inc_handler: Counter to increment when the function is called.
        hist_handler: Histogram to observe the execution time of the function.
        exc_handler: Counter to increment when the function raises an exception.
        counter_labels: Labels to add to the counter.
        hist_labels: Labels to add to the histogram.
        exc_labels: Labels to add to the exception counter.

    Usage:
        @meta_monitor(
            inc_handler=RequestCounter,
            hist_handler=RequestDurationHistogram,
            exc_handler=ExceptionCounter,
            counter_labels=["foo", "bar"],
            hist_labels=["foo2", "bar2"],
            exc_labels=["foo3", "bar3"],
        )
        def my_function(*args, **kwargs) -> t.Any:
            pass


    """

    def decorator(func: t.Callable) -> t.Callable:
        @wraps(func)
        async def wrapper(*args: t.Any, **kwargs: t.Any) -> t.Any:
            if counter_handler:
                new_counter_labels = counter_labels or []
                counter_str_labels = [
                    label(func, *args, **kwargs) if callable(label) else label
                    for label in new_counter_labels
                ]
                counter_handler_target = counter_handler.labels(*counter_str_labels)
            else:
                counter_handler_target = None

            if hist_handler:
                new_hist_labels = hist_labels or []
                hist_str_labels = [
                    label(func, *args, **kwargs) if callable(label) else label
                    for label in new_hist_labels
                ]
                hist_handler_target = hist_handler.labels(*hist_str_labels)
            else:
                hist_handler_target = None

            if exc_handler:
                new_exc_labels = exc_labels or []
                exc_str_labels = [
                    label(func, *args, **kwargs) if callable(label) else label
                    for label in new_exc_labels
                ]
                exc_handler_target = exc_handler.labels(*exc_str_labels)
            else:
                exc_handler_target = None

            if counter_handler_target:
                counter_handler_target.inc()

            async def _wrapper() -> t.Any:
                try:
                    return await func(*args, **kwargs)
                except Exception as err:
                    if exc_handler_target:
                        exc_handler_target.inc()
                    raise err

            if hist_handler_target:
                with hist_handler_target.time():
                    return await _wrapper()
            else:
                return await _wrapper()

        @wraps(func)
        def sync_wrapper(*args: t.Any, **kwargs: t.Any) -> t.Any:
            if counter_handler:
                new_counter_labels = counter_labels or []
                counter_str_labels = [
                    label(func, *args, **kwargs) if callable(label) else label
                    for label in new_counter_labels
                ]
                counter_handler_target = counter_handler.labels(*counter_str_labels)
            else:
                counter_handler_target = None

            if hist_handler:
                new_hist_labels = hist_labels or []
                hist_str_labels = [
                    label(func, *args, **kwargs) if callable(label) else label
                    for label in new_hist_labels
                ]
                hist_handler_target = hist_handler.labels(*hist_str_labels)
            else:
                hist_handler_target = None

            if exc_handler:
                new_exc_labels = exc_labels or []
                exc_str_labels = [
                    label(func, *args, **kwargs) if callable(label) else label
                    for label in new_exc_labels
                ]
                exc_handler_target = exc_handler.labels(*exc_str_labels)
            else:
                exc_handler_target = None

            if counter_handler_target:
                counter_handler_target.inc()

            def _wrapper() -> t.Any:
                try:
                    return func(*args, **kwargs)
                except Exception as err:
                    if exc_handler_target:
                        exc_handler_target.inc()
                    raise err

            if hist_handler_target:
                with hist_handler_target.time():
                    return _wrapper()
            else:
                return _wrapper()

        return wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return decorator
