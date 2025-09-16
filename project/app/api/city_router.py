from typing import List

from fastapi import APIRouter

from app.schemas.city_schema import CityOutputSchema
from app.services.city_service import CityService

router = APIRouter()


@router.get("", responses={200: {"model": CityOutputSchema}})
async def read_all_cities() -> List[CityOutputSchema]:
    """method to get all cities"""
    cities = await CityService.get_all_cities()

    return cities
