import sys
import os
import pytest
from requests.models import Response
from starlette.testclient import TestClient
from app.services.user_service import UserService
sys.path.append(os.path.dirname(__file__))
from test_demo_data import VALID_USER_DATA

class TestMe:



    @pytest.fixture(autouse=True)
    def _request_test_app_db(self, test_app_db):
        self._test_app_db = test_app_db

    @staticmethod
    def generate_test_token(user_id: int) -> str:
        """
        Method that generates a valid token to test the methods that require authentication
        """

        token, _ = UserService._generate_token(user_id=user_id, duration=500000000)
        return token

    def test_get_me(self):

        token = self.generate_test_token(user_id=2)
        response = self._test_app_db.get("/me", headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200
        response_json = response.json()

        assert "id" in response_json
        assert "nickname" in response_json
        assert "birthdate" in response_json
        assert "name" in response_json
        assert "surname" in response_json
        assert "description" in response_json

    def test_get_me_invalid_token(self):

        token = "invalidtoken"
        response = self._test_app_db.get("/me", headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 409
        
        
        

        

