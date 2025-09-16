from typing import Any, Dict

from fastapi import APIRouter, Depends

from app.api import AuthBearer
from app.schemas.user_schema import UserOutputSchema
from app.services.user_service import UserService

router = APIRouter()


@router.get("", responses={200: {"model": UserOutputSchema}})
async def get_me(
    user_info: Dict[str, Any] = Depends(AuthBearer())
) -> UserOutputSchema:  # noqa: E501
    user_response = await UserService.get_me(
        user_info["token"], user_info["user_id"]
    )  # noqa: E501

    return user_response
