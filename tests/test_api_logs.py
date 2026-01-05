def test_get_logs(client):
    response = client.get("/logs")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_log_created_after_anesthesia(client):
    payload = {
        "name": "Test",
        "age": 45,
        "weight": 76,
        "asa_class": "II",
        "anesthesia_type": "combined"
    }
    client.post("/anesthesia", json=payload)
    logs = client.get("/logs").get_json()

    assert len(logs) > 0