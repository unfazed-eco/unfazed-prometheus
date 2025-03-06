import pytest
from prometheus_client import Counter, Histogram

from unfazed_prometheus.decorators import meta_monitor


async def test_counter_handler() -> None:
    counter = Counter("test_counter", "test counter", labelnames=["test"])

    @meta_monitor(counter_handler=counter, counter_labels=["counter_label"])
    async def test_func() -> None:
        pass

    await test_func()
    assert counter.labels("counter_label")._value._value == 1.0

    await test_func()
    assert counter.labels("counter_label")._value._value == 2.0

    @meta_monitor(counter_handler=counter, counter_labels=["counter_label2"])
    def test_func2() -> None:
        pass

    test_func2()
    assert counter.labels("counter_label2")._value._value == 1.0


async def test_hist_handler() -> None:
    hist = Histogram("test_hist", "test hist", labelnames=["test"])

    @meta_monitor(hist_handler=hist, hist_labels=["hist_label"])
    async def test_func() -> None:
        pass

    await test_func()
    assert hist.labels("hist_label")._buckets[0]._value == 1.0

    await test_func()
    assert hist.labels("hist_label")._buckets[0]._value == 2.0

    @meta_monitor(hist_handler=hist, hist_labels=["hist_label2"])
    def test_func2() -> None:
        pass

    test_func2()
    assert hist.labels("hist_label2")._buckets[0]._value == 1.0


async def test_exc_handler() -> None:
    exc = Counter("test_exc", "test exc", labelnames=["test"])

    @meta_monitor(exc_handler=exc, exc_labels=["exc_label"])
    async def test_func() -> None:
        raise ValueError("test exc")

    with pytest.raises(ValueError):
        await test_func()

    assert exc.labels("exc_label")._value._value == 1.0
