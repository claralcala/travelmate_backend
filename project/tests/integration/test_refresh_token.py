import pytest
from app.services.user_service import UserService

@pytest.mark.usefixtures("test_app_db")
class TestRefresh:


    @pytest.fixture(autouse=True)
    def _request_test_app_db(self, test_app_db):
        self._test_app_db = test_app_db

    
    @staticmethod
    def generate_test_token(user_id: int) -> str:
        """
        Method that generates a valid token to test the methods that require authentication
        """
        token, _ = UserService._generate_token(user_id=user_id, duration=5000)
        return token
    

    def test_refresh_token(self):
        refresh_token = TestRefresh.generate_test_token(user_id=1)
        
        payload = {
            "refresh_token": refresh_token
        }

        response = self._test_app_db.post("/refreshToken", json=payload)

        assert response.status_code == 200
        response_json = response.json()
        

        assert "token" in response_json
        assert "expire_token" in response_json
        assert "refresh_token" in response_json
        assert "expire_refresh_token" in response_json

    def test_refresh_token_invalid(self):
        refresh_token = "invalidtoken"
        
        payload = {
            "refresh_token": refresh_token
        }

        response = self._test_app_db.post("/refreshToken", json=payload)

        assert response.status_code == 412
        response_json = response.json()
        

        assert "detail" in response_json
        assert response_json["detail"] == "The refresh token provided is not valid"
        