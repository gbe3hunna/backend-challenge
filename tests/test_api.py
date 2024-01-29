import pytest
from fastapi.testclient import TestClient
from fastapi import status
from src.api.main import app


@pytest.fixture(name="test_client", scope="module", autouse=True)
def test_client():
    client = TestClient(app)
    yield client


class TestAPI:
    def test_root_endpoint_returns_404(self, test_client: TestClient):
        response = test_client.get("/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

