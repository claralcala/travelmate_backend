from typing import Any, Dict

from fastapi import APIRouter, Depends

from app.api import AuthBearer
from app.schemas.app_schema import AppEmptyOutputSchema
from app.services.user_service import UserService

router = APIRouter()


@router.post("")
async def logout(
    user_info: Dict[str, Any] = Depends(AuthBearer())
) -> AppEmptyOutputSchema:
    await UserService.logout_user(user_info["token"])

    return AppEmptyOutputSchema()
