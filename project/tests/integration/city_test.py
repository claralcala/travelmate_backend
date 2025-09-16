import pytest
from requests.models import Response
from starlette.testclient import TestClient

@pytest.mark.usefixtures("test_app_db")
class TestCity:



    @pytest.fixture(autouse=True)
    def _request_test_app_db(self, test_app_db):
        self._test_app_db = test_app_db

    
    def test_read_all_cities_count(self):
        response = self._test_app_db.get("/cities")

        assert response.status_code == 200
        response_json = response.json()
        assert len(response_json) == 1026
    
    def test_contains_specific_city(self):

        city_name = "Madrid"
        response = self._test_app_db.get("/cities")

        assert response.status_code == 200
        response_json = response.json()
        city_names = [city["name"] for city in response_json]
        assert city_name in city_names
