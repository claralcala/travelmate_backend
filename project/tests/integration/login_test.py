import sys
import os
import pytest
from requests.models import Response
from starlette.testclient import TestClient
sys.path.append(os.path.dirname(__file__))
from test_demo_data import CORRECT_LOGIN, INCORRECT_LOGIN

@pytest.mark.usefixtures("test_app_db")
class TestLogin:



    @pytest.fixture(autouse=True)
    def _request_test_app_db(self, test_app_db):
        self._test_app_db = test_app_db

    def test_login(self):
        response = self._test_app_db.post("/login", json= CORRECT_LOGIN)

        assert response.status_code == 200
        response_json = response.json()
        assert "token" in response_json
        assert "expire_token" in response_json

    def test_incorrect_login(self):
        response = self._test_app_db.post("/login", json= INCORRECT_LOGIN)

        assert response.status_code == 407
        response_json = response.json()
        assert "detail" in response_json
        assert response_json["detail"] == "User not found"