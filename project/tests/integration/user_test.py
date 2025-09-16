import sys
import os
import json

import pytest
from requests.models import Response
from starlette.testclient import TestClient
sys.path.append(os.path.dirname(__file__))
from test_demo_data import VALID_USER_DATA, INVALID_USER_DATA, EXISTING_USER_DATA, MISSING_FIELD_USER_DATA, EXISTING_USERNAME_DATA

@pytest.mark.usefixtures("test_app_db")
class TestUser:




    @pytest.fixture(autouse=True)
    def _request_test_app_db(self, test_app_db):
        self._test_app_db = test_app_db


    def test_register_user(self):
        """
        Test to register an user succesfully (valid data)
        """
        
        response= self._test_app_db.post("/user/register", json=VALID_USER_DATA)

        assert response.status_code == 200
        # checking if the json contains token
        assert "token" in response.json()
        assert "expire_token" in response.json()

    

    def test_register_invalid_data(self):
        response= self._test_app_db.post("/user/register", json= INVALID_USER_DATA)

        assert response.status_code == 422
        response_json = response.json()
        assert "detail" in response_json

        detail = response_json["detail"]
        error_message = "Value error, Password must have at least 8 characters, include 1 lowercase letter, 1 uppercase letter and 1 non alphanumeric character"
        assert any(error["msg"] == error_message for error in detail)


    def test_register_existing_email(self):
        response= self._test_app_db.post("/user/register", json= EXISTING_USER_DATA)

        assert response.status_code == 402
        response_json = response.json()
        assert "detail" in response_json
        assert response_json["detail"] == "Email already in use"

    def test_register_existing_username(self):
        response= self._test_app_db.post("/user/register", json= EXISTING_USERNAME_DATA)

        assert response.status_code == 405
        response_json = response.json()
        assert "detail" in response_json
        assert response_json["detail"] == "Nickname already in use"

    def test_register_missing_field(self):
        response= self._test_app_db.post("/user/register", json= MISSING_FIELD_USER_DATA)

        assert response.status_code == 422
        response_json = response.json()
        assert "detail" in response_json
        assert isinstance(response_json["detail"], list)
        assert len(response_json["detail"]) > 0

        error_detail = response_json["detail"][0]
        assert error_detail["loc"] == ["body", "email"]
        assert error_detail["msg"] == "Field required"
        assert error_detail["type"] == "missing"
