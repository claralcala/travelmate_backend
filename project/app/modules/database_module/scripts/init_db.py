import logging
import os

from tortoise import Tortoise, run_async

from app.modules.database_module.scripts.import_cities import import_cities

logger = logging.getLogger(__name__)


async def generate_schema() -> None:
    """
    Generate the schema in database from model
    """
    logger.info("Initializing Tortoise...")

    await Tortoise.init(
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ["app.modules.database_module.models"]},
    )

    logger.info("Generating database schema via Tortoise...")
    await Tortoise.generate_schemas()
    logger.info("Inserting cities...")
    await import_cities()
    await Tortoise.close_connections()


if __name__ == "__main__":
    run_async(generate_schema())
