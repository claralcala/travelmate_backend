from typing import Any, Dict

from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.services.user_service import UserService
from app.services.user_service_exception import (
    UserServiceException,
    UserServiceExceptionInfo,
)

user_service = UserService()


class AuthBearer(HTTPBearer):
    """
    Class to secure the API routes
    """

    def __init__(self) -> None:
        super(AuthBearer, self).__init__(auto_error=False)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            AuthBearer, self
        ).__call__(request)
        if credentials and credentials.scheme == "Bearer":
            return await self.verify_token(credentials.credentials)
        else:
            raise UserServiceException(
                UserServiceExceptionInfo.INVALID_AUTHENTICATION_SCHEME
            )

    @staticmethod
    async def verify_token(token: str) -> Dict[str, Any]:
        """
        Verifies the token passed by parameter:
        :param token: token to verify
        :return: token information if is valid
        :rtype: Dict[str, Any]
        """
        payload = await user_service.is_valid_token(token)

        if payload:
            return {**payload, **{"token": token}}
        raise UserServiceException(
            UserServiceExceptionInfo.INVALID_AUTHENTICATION_TOKEN
        )
