import os
import typing as t

import pytest
from unfazed.core import Unfazed
from unfazed.test import Requestfactory

from unfazed_prometheus import agent


@pytest.fixture(scope="session")
def setup_db_state() -> t.Generator[None, None, None]:
    # delete all file suffix with .db in /prometheus
    for file in os.listdir("/prometheus"):
        if file.endswith(".db"):
            os.remove(os.path.join("/prometheus", file))

    yield

    # delete all db file in /prometheus
    for file in os.listdir("/prometheus"):
        if file.endswith(".db"):
            os.remove(os.path.join("/prometheus", file))


async def assert_db_files_exist() -> None:
    assert len(os.listdir("/prometheus")) > 0
    flag = False
    for file in os.listdir("/prometheus"):
        if file.endswith(".db"):
            flag = True
            # check file size is not 0
            assert os.path.getsize(os.path.join("/prometheus", file)) > 0

    assert flag, "no db files found"


async def test_requests(
    unfazed: Unfazed,
    setup_db_state: t.Generator[None, None, None],
) -> None:
    async with Requestfactory(unfazed) as rf:
        for i in range(100):
            resp = await rf.get("/api/hello1")
            assert resp.status_code == 200

            resp = await rf.get("/api/hello2")
            assert resp.status_code == 200

    await assert_db_files_exist()


async def test_api_call(
    setup_db_state: t.Generator[None, None, None],
) -> None:
    @agent.monitor_api("/api/call/hello1")
    async def hello1():
        return "hello1"

    @agent.monitor_api("/api/call/hello2")
    async def hello2():
        return "hello2"

    for i in range(100):
        resp = await hello1()
        assert resp == "hello1"

        resp = await hello2()
        assert resp == "hello2"

    await assert_db_files_exist()


async def test_function_call(
    setup_db_state: t.Generator[None, None, None],
) -> None:
    @agent.monitor_function
    async def func1():
        return "func1"

    @agent.monitor_function
    async def _func2():
        raise Exception("func2 error")

    async def func2():
        try:
            await _func2()
        except Exception as e:
            return str(e)

    @agent.monitor_function
    def func3():
        return "func3"

    @agent.monitor_function
    def _func4():
        raise Exception("func4 error")

    def func4():
        try:
            _func4()
        except Exception as e:
            return str(e)

    for i in range(100):
        await func1()
        await func2()
        func3()
        func4()

    await assert_db_files_exist()


async def test_db(
    unfazed: Unfazed,
    setup_db_state: t.Generator[None, None, None],
) -> None:
    async with Requestfactory(unfazed) as rf:
        resp = await rf.get("/api/app/user-list")
        assert resp.status_code == 200

        resp = await rf.get("/api/app/user-create")
        assert resp.status_code == 200

    await assert_db_files_exist()


async def test_cache(
    unfazed: Unfazed,
    setup_db_state: t.Generator[None, None, None],
) -> None:
    async with Requestfactory(unfazed) as rf:
        resp = await rf.get("/api/app/cache-get")
        assert resp.status_code == 200

        resp = await rf.get("/api/app/cache-set")
        assert resp.status_code == 200

    await assert_db_files_exist()
