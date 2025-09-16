from fastapi import APIRouter

from app.schemas.refresh_token_schema import (
    RefreshTokenInputSchema,
    RefreshTokenOutputSchema,
)
from app.services.user_service import UserService

router = APIRouter()


@router.post("", responses={200: {"model": RefreshTokenOutputSchema}})
async def refresh_token(
    payload: RefreshTokenInputSchema,
) -> RefreshTokenOutputSchema:
    token_output = await UserService.refresh_user_token(payload.refresh_token)

    return token_output
