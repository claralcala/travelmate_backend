import sys
import os
import pytest
from requests.models import Response
from starlette.testclient import TestClient
from app.schemas.pagination_schema import PaginationOutputSchema
from app.schemas.trip_schema import TripOutputSchema
from app.services.user_service import UserService
sys.path.append(os.path.dirname(__file__))
from test_demo_data import TRIP_DATA

@pytest.mark.usefixtures("test_app_db")
class TestTrip:


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
    
    def test_create_trip(self):
        
        token = TestTrip.generate_test_token(user_id=2)

        response = self._test_app_db.post("/trips/create", json= TRIP_DATA, headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200


        response_json = response.json()

        assert response_json["origin"]["id"] == TRIP_DATA["origin"]
        assert response_json["destination"]["id"] == TRIP_DATA["destination"]
        assert response_json["start_date"] == TRIP_DATA["start_date"]
        assert response_json["end_date"] == TRIP_DATA["end_date"]
        assert response_json["description"] == TRIP_DATA["description"]
        assert len(response_json["transportation_methods"]) == len(TRIP_DATA["transportation_method_ids"])

        for method_id in TRIP_DATA["transportation_method_ids"]:
           assert any(method["id"] == method_id for method in response_json["transportation_methods"])
    
    def test_get_trip(self):
        trip_id = 11
        response = self._test_app_db.get(f"/trips/{trip_id}")
        assert response.status_code == 200

        response_json = response.json()

        assert "origin" in response_json
        assert "destination" in response_json
        assert "number_of_participants" in response_json
        assert "creator" in response_json

    def test_get_trip_doesnt_exist(self):
        trip_id = 11111111
        response = self._test_app_db.get(f"/trips/{trip_id}")
        assert response.status_code == 1005

        
    
    def test_join_trip(self):

        token = TestTrip.generate_test_token(user_id=3)

        trip_id = 65

        response = self._test_app_db.post(f"/trips/{trip_id}/joinTrip", headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200

    def test_join_trip_user_already_joined(self):

        token = TestTrip.generate_test_token(user_id=3)

        trip_id = 65

        response = self._test_app_db.post(f"/trips/{trip_id}/joinTrip", headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 1004

    def test_unjoin_trip(self):

        token = TestTrip.generate_test_token(user_id=3)

        trip_id = 65

        response = self._test_app_db.delete(f"/trips/{trip_id}/unjoinTrip", headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200

    
    def test_delete_trip(self):

        token = TestTrip.generate_test_token(user_id=2)

        trip_id = 108
        response = self._test_app_db.delete(f"/trips/{trip_id}/deleteTrip", headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200


    def test_delete_trip_doesnt_exist(self):

        token = TestTrip.generate_test_token(user_id=2)

        trip_id = 60000
        response = self._test_app_db.delete(f"/trips/{trip_id}/deleteTrip", headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 1005


    def test_delete_trip_not_creator(self):

        token = TestTrip.generate_test_token(user_id=2)

        trip_id = 11
        response = self._test_app_db.delete(f"/trips/{trip_id}/deleteTrip", headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 1007


    def test_pagination(self):
        response = self._test_app_db.get("/trips")
        assert response.status_code == 200
        response_json = response.json()

        # Checking if the pagination schema is correct
        assert "page_number" in response_json
        assert "page_size" in response_json
        assert "total_pages" in response_json
        assert "total_record" in response_json
        assert "content" in response_json

        
        assert response_json["page_number"] == 1
        assert response_json["page_size"] == 10

