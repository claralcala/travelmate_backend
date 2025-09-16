from fastapi import APIRouter, status
from fastapi.responses import Response

from app.schemas.forgot_password_schema import ForgotPasswordInputSchema
from app.services.user_service import UserService

router = APIRouter()


@router.post("")
async def forgot_password(payload: ForgotPasswordInputSchema):

    await UserService.user_forgot_password(payload.email)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
