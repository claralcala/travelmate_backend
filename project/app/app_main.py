import logging
import os

import uvicorn
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from tortoise.contrib.fastapi import register_tortoise

from app import app_config
from app.api import (
    city_router,
    forgot_password_router,
    login_router,
    logout_router,
    me_router,
    refresh_token_router,
    trip_router,
    user_router,
)
from app.modules.email_module import register_email
from app.modules.firebase_module import register_firebase
from app.schemas.app_schema import AppErrorOutputSchema, AppException

# flake8: noqa

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def init_db(application: FastAPI) -> None:
    """
    Init the ORM database
    """
    register_tortoise(
        application,
        db_url=os.environ.get("DATABASE_URL"),
        # Route to database modules
        modules={"models": ["app.modules.database_module.models"]},
        generate_schemas=True,
        add_exception_handlers=False,
    )


def init_email() -> None:
    """
    Init the Email module
    """
    register_email(
        smtp_host=app_config.smtp_host,
        smtp_port=app_config.smtp_port,
        smtp_user=app_config.smtp_user,
        smtp_password=app_config.smtp_password,
        environment="dev",
    )


def init_firebase() -> None:
    """
    Init the Firebase module
    """
    register_firebase()


def create_application() -> FastAPI:
    """
    Create the application and return it
    :return: Application instance
    :rtype: FastAPI
    """
    application = FastAPI(
        title="Travel Mate project",
        description="Travel Mate is an application aimed at people "
        "that don't want to travel alone",
        version="1.0",
    )

    # Routes
    application.include_router(user_router.router, prefix="/user", tags=["Users"])
    application.include_router(trip_router.router, prefix="/trips", tags=["Trips"])
    application.include_router(login_router.router, prefix="/login", tags=["Login"])
    application.include_router(
        forgot_password_router.router,
        prefix="/forgotPassword",
        tags=["Forgot Password"],
    )
    application.include_router(city_router.router, prefix="/cities", tags=["Cities"])
    application.include_router(me_router.router, prefix="/me", tags=["Me"])
    application.include_router(logout_router.router, prefix="/logout", tags=["Logout"])
    application.include_router(
        refresh_token_router.router, prefix="/refreshToken", tags=["Refresh Token"]
    )

    return application


app = create_application()


@app.on_event("startup")
async def startup_event() -> None:
    """
    Define a handler that will be executed before the app starts up
    """
    logger.info("Starting up...")
    init_db(app)
    init_email()
    init_firebase()


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """
    Define a handler that will be executed before the app shutting down
    """
    logger.info("Shutting down...")


@app.exception_handler(AppException)
async def application_service_handler(_request: Request, exception: AppException):

    return JSONResponse(
        status_code=exception.http_code,
        content=jsonable_encoder(
            obj=AppErrorOutputSchema(
                code=exception.status_code, error=exception.detail
            ),
            exclude_none=True,
        ),
    )


@app.exception_handler(ValueError)
async def application_unexpected_exception_handler(
    _request: Request, exception: ValueError
):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder(
            obj=AppErrorOutputSchema(code=422, error=str(exception)), exclude_none=True
        ),
    )


@app.exception_handler(RequestValidationError)
async def application_unexpected_exception_handler(
    _request: Request, exception: ValidationError
):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder(
            obj=AppErrorOutputSchema(code=422, error=exception.errors()[0]["msg"]),
            exclude_none=True,
        ),
    )


@app.exception_handler(Exception)
async def application_unexpected_exception_handler(
    _request: Request, _exception: Exception
):
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder(
            obj=AppErrorOutputSchema(
                code=500,
                error="An unexpected error occurred. "
                "Contact with the server's administrator",
            ),
            exclude_none=True,
        ),
    )


# ONLY FOR DEVELOPMENT
if __name__ == "__main__":
    uvicorn.run("app_main:app", host="0.0.0.0", port=8000, reload=False)
