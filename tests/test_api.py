def test_generate_combined_anesthesia(client):
    payload = {
        "name": "Test Patient",
        "age": 40,
        "weight": 70,
        "asa_class": "I",
        "anesthesia_type": "combined"
    }

    response = client.post("/anesthesia", json=payload)

    assert response.status_code == 200
    data = response.get_json()

    assert "protocol" in data
    assert "doses" in data

    assert "Propofol" in data["protocol"]
    assert "fentanyl" in data["doses"]

def test_generate_spinal_anesthesia(client):
    payload = {
        "name": "Test Patient",
        "age": 50,
        "weight": 80,
        "asa_class": "II",
        "anesthesia_type": "regional",
        "block_type": "spinal"
    }
    response = client.post("/anesthesia", json=payload)

    assert response.status_code == 200
    data = response.get_json()

    assert "Bupivacaine" in data["protocol"]
    assert "max_safe_dose" in data["doses"]

def test_generate_epidural_anesthesia(client):
    payload = {
        "name": "Test Patient",
        "age": 60,
        "weight": 90,
        "asa_class": "III",
        "anesthesia_type": "regional",
        "block_type": "epidural"
    }

    response = client.post("/anesthesia", json=payload)

    assert response.status_code == 200
    data = response.get_json()

    assert "Epidural" in data["protocol"]
