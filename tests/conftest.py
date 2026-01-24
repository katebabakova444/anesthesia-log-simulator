import pytest
from anesthesia.app import app
import os

@pytest.fixture
def client(tmp_path):
    test_db_path = tmp_path / "test_anesthesia.db"
    app.config["TESTING"] = True

    app.config["DATABASE"] = test_db_path

    with app.test_client() as client:
        yield client

    if os.path.exists(test_db_path):
        os.remove(test_db_path)
