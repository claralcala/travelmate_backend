from typing import Any, Dict, Union

from pydantic import EmailStr
from tortoise.exceptions import DoesNotExist

from app.modules.database_module.models import Token, User
from app.services.user_service_exception import (
    UserServiceException,
    UserServiceExceptionInfo,
)
from app.utils.security import get_password_hash, verify_password


class UserRepository:

    @staticmethod
    async def email_exists(email: str) -> bool:
        return await User.exists(email=email.lower())

    @staticmethod
    async def nickname_exists(nickname: str) -> bool:
        return await User.exists(nickname=nickname)

    @staticmethod
    async def create_user(user_info: Dict[str, Any]) -> User:

        # hashing the password before inserting it into the database
        user_info["password"] = get_password_hash(user_info["password"])
        user_info["email"] = user_info["email"].lower()
        user = await User.create(**user_info)
        return user

    @staticmethod
    async def user_login(email: EmailStr, password: str) -> Union[int, None]:

        user = await User.get_or_none(email=email.lower())
        if user is None:
            raise UserServiceException(UserServiceExceptionInfo.INVALID_USER)
        if verify_password(password, user.password):
            return user.id
        else:
            raise UserServiceException(
                UserServiceExceptionInfo.INCORRECT_PASSWORD
            )  # noqa: E501

    @staticmethod
    async def get_user(email: EmailStr) -> Union[int, None]:
        """
        Method to get specific user by their email
        return: the user's id
        """
        user = await User.get_or_none(email=email.lower())
        if user is None:
            return None
        else:
            return user.id

    @staticmethod
    async def get_user_by_id(user_id: int) -> User:
        """
        Method to get specific user by their email
        return: the user's id
        """
        user = await User.get(id=user_id)
        return user

    @staticmethod
    async def update_password(user_id: int, new_pwd: str) -> bool:
        """Update the password for a user by their user_id
        Returns true if the password is changed, false otherwise

        """
        try:

            user = await User.get(id=user_id)
            new_pwd = get_password_hash(new_pwd)
            # Hash the password
            user.password = new_pwd
            await user.save()
            return True

        except DoesNotExist:

            return False

    @staticmethod
    async def insert_token(
        user_id: int, token: str, refresh_token: str
    ) -> None:  # noqa: E501
        await Token.create(
            user_id=user_id, token=token, refresh_token=refresh_token
        )  # noqa: E501

    @staticmethod
    async def update_token(
        token: str, refresh_token: str, filters: Dict[str, Any]
    ) -> None:
        await Token.filter(**filters).update(
            token=token, refresh_token=refresh_token
        )  # noqa: E501

    @staticmethod
    async def logout_user(token: str) -> None:
        await Token.filter(token=token).delete()

    @staticmethod
    async def update_user_profile_photo(user_id: int, photo_url: str):
        user = await UserRepository.get_user_by_id(user_id=user_id)
        user.photo = photo_url

        await user.save()
