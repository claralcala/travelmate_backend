import json
import logging
import os

from tortoise import Tortoise, run_async
from tortoise.exceptions import IntegrityError

from app.modules.database_module.models.city_model import City

logger = logging.getLogger(__name__)


async def init():

    await Tortoise.init(
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ["app.modules.database_module.models"]},
    )

    await Tortoise.generate_schemas()


async def import_cities():

    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "top-1000-cities.json")

    with open(file_path, "r") as f:
        cities = json.load(f)

    for city in cities:
        existing_city = await City.get_or_none(name=city["name"])
        if existing_city is None:
            try:
                await City.create(name=city["name"], country=city["country"])
                logger.info(f"City {city['name']} created")
            except IntegrityError as e:
                logger.error(f"Failed to insert city {city['name']}: {e}")
        else:
            logger.info(f"City {city['name']} already exists in db")

    logger.info("Cities have been imported succesfully")


async def call_cities():
    await init()
    await import_cities()


if __name__ == "__main__":
    run_async(call_cities())
