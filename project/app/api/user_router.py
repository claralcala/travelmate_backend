from fastapi import APIRouter

from app.schemas.login_schema import LoginOutputSchema
from app.schemas.user_schema import UserInputSchema
from app.services.user_service import (
    UserService,
    UserServiceException,
    UserServiceExceptionInfo,
)

router = APIRouter()


@router.post("/register", responses={200: {"model": LoginOutputSchema}})
async def register_user(payload: UserInputSchema) -> LoginOutputSchema:
    """method to register a new user & automathically log them in"""

    user = await UserService.post_user(payload)

    # Calling the method user_login with user mail and password to autolog
    # after registering and immediately returning the user two tokens
    autologin = await UserService.user_login(user.email, payload.password)
    if autologin is None:
        raise UserServiceException(UserServiceExceptionInfo.LOGIN_FAILED)

    return autologin
