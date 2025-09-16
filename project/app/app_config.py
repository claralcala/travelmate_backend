import logging
import os
from functools import lru_cache

from pydantic import AnyUrl
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)


class ApplicationSettings(BaseSettings):
    """
    Class with different settings of the application
    """

    environment: str = os.getenv("ENVIRONMENT", "dev")
    testing: bool = os.getenv("TESTING", 0)
    database_url: AnyUrl = os.environ.get("DATABASE_URL")

    # TOKENS
    token_expiration: int = os.getenv("TOKEN_EXPIRATION_TIME", 3600 * 24 * 30)
    rt_expiration_time: int = os.getenv(
        "REFRESH_TOKEN_EXPIRATION_TIME", 3600 * 24 * 90
    )  # noqa: E501
    token_secret_key: str = os.getenv("TOKEN_SECRET_KEY")

    # SMTP_CONFIG
    smtp_host: str = os.getenv("SMTP_HOST")
    smtp_user: str = os.getenv("SMTP_USER")
    smtp_port: str = os.getenv("SMTP_PORT")
    smtp_password: str = os.getenv("SMTP_PASSWORD")


@lru_cache()  # Cache the settings
def get_application_settings() -> ApplicationSettings:
    """
    Instance the ApplicationSettings and return it
    :return: Object with the application's configuration
    :rtype: ApplicationSettings
    """
    logger.info("Loading configuration settings from the environment...")
    return ApplicationSettings()
