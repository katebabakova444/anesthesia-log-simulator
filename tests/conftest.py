import pytest
from anesthesia.app import app
import os
TEST_DB = "test_anesthesia.db"

@pytest.fixture
def client():
    app.config["TESTING"] = True

    app.config["DATABASE"] = TEST_DB

    with app.test_client() as client:
        yield client

    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
