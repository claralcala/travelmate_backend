import sys
import os
import pytest
from requests.models import Response
from starlette.testclient import TestClient
from app.modules.email_module import EmailModule
sys.path.append(os.path.dirname(__file__))
from test_demo_data import FORGOT_PASSWORD



@pytest.mark.usefixtures("test_app_db")
class TestForgotPassword:
    


    @pytest.fixture(autouse=True)
    def _request_test_app_db(self, test_app_db):
        self._test_app_db = test_app_db

    
    

    def test_forgot_password_response(self):
        response = self._test_app_db.post("/forgotPassword", json= FORGOT_PASSWORD)

        assert response.status_code == 204
