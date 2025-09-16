import pytest
from app.services.user_service import UserService

@pytest.mark.usefixtures("test_app_db")
class TestLogout:


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
    

    def test_logout(self):
        token = self.generate_test_token(user_id=2)


        response = self._test_app_db.post("/logout", headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200
        
    
    

