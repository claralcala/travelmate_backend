from typing import List

from app.repositories.city_repository import CityRepository
from app.schemas.city_schema import CityOutputSchema


class CityService:

    async def get_all_cities() -> List[CityOutputSchema]:
        cities_info = await CityRepository.read_all_cities()

        cities_result_list = []
        for city in cities_info:
            city_schema = CityOutputSchema(
                id=city.id, name=city.name, country=city.country
            )
            cities_result_list.append(city_schema)
        return cities_result_list
