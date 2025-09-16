from fastapi import APIRouter

from app.schemas.login_schema import LoginInputSchema, LoginOutputSchema
from app.services.user_service import UserService

router = APIRouter()


@router.post("", responses={200: {"model": LoginOutputSchema}})
async def login(payload: LoginInputSchema) -> LoginOutputSchema:
    """
    HTTP POST method to log in an user
    """

    return await UserService.user_login(payload.email, payload.password)
