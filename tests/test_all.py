from unfazed.core import Unfazed
from unfazed.test import Requestfactory


async def test_requests(unfazed: Unfazed) -> None:
    async with Requestfactory(unfazed) as rf:
        for i in range(100):
            resp = await rf.get("/api/hello1")
            assert resp.status_code == 200

            resp = await rf.get("/api/hello2")
            assert resp.status_code == 200
