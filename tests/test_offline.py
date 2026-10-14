import pytest

@pytest.mark.asyncio
async def test_offline_sync(client):
    m = await client.post("/api/messages", json={"content": "Hello offline"})
    assert m.status_code == 200
    q = await client.get("/api/queue")
    assert q.json()["pending"] >= 2
    s = await client.post("/api/sync")
    assert s.json()["synced"] >= 2
    q2 = await client.get("/api/queue")
    assert q2.json()["pending"] == 0
