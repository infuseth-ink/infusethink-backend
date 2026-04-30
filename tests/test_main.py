from fastapi.testclient import TestClient
import pytest

from src.main import app


class TestNested:
    class TestRoot:
        @pytest.fixture(name="client")
        def client_fixture(self):
            yield TestClient(app)

        def test_returns_200(self, client):
            response = client.get("/")
            assert response.status_code == 200

        def test_includes_git_sha_in_response(self, client):
            response = client.get("/")
            assert "git_sha" in response.json()

    class TestDummy:
        def test_addition(self):
            assert 1 + 2 == 3

        def test_subtraction(self):
            assert 3 - 1 == 2
