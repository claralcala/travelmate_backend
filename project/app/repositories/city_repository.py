from typing import List

from app.modules.database_module.models.city_model import City
from app.repositories.app_repository import AppRepository


class CityRepository(AppRepository):

    @staticmethod
    async def read_all_cities() -> List[City]:

        cities_info = await City.all().order_by('name')

        return cities_info

    @staticmethod
    async def read_city(city_id: int) -> City:
        """
        Method to get specific city by its id
        """
        city = await City.get(id=city_id)
        return city
