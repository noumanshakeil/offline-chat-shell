from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["service"] == "offline-chat-shell"


def test_list_and_action():
    r = client.get("/api/queues")
    assert r.status_code == 200
    assert "queues" in r.json()

    r2 = client.post("/api/local_reply", json={"prompt": "smoke test"})
    assert r2.status_code == 200
    body = r2.json()
    assert body["ok"] is True
    assert "result" in body
