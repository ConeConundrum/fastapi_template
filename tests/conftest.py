import pytest
from faker import Faker
from fastapi.testclient import TestClient

faker = Faker()


@pytest.fixture(scope='session')
def client():
    """Test app client"""
    from app.main import app
    with TestClient(app) as client:
        yield client
