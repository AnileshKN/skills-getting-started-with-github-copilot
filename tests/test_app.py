from fastapi.testclient import TestClient
from src.app import app


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Basketball" in data


def test_signup_and_unregister_workflow():
    activity = "Basketball"
    email = "tester@example.com"

    # Ensure clean state: remove test email if present
    current = client.get("/activities").json()
    if email in current.get(activity, {}).get("participants", []):
        client.post(f"/activities/{activity}/unregister", params={"email": email})

    # Sign up
    r = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r.status_code == 200
    assert "Signed up" in r.json().get("message", "")

    # Verify participant present
    after = client.get("/activities").json()
    assert email in after[activity]["participants"]

    # Unregister
    r2 = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert r2.status_code == 200

    # Verify removed
    final = client.get("/activities").json()
    assert email not in final[activity]["participants"]
