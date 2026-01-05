def test_invalid_anesthesia_type(client):
    payload = {
        "name": "Test",
        "age": 30,
        "weight": 70,
        "asa_class": "I",
        "anesthesia_type": "magic"
    }
    response = client.post("/anesthesia", json=payload)
    assert response.status_code == 400

def test_regional_without_block_type(client):
    payload = {
        "name": "Test",
        "age": 30,
        "weight": 70,
        "asa_class": "I",
        "anesthesia_type": "regional"
    }
    response = client.post("/anesthesia", json=payload)
    assert response.status_code == 400

def test_invalid_weight(client):
    payload = {
        "name": "Test",
        "age": 30,
        "weight": -20,
        "asa_class": "I",
        "anesthesia_type": "combined"
    }
    response = client.post("/anesthesia", json=payload)
    assert response.status_code == 400