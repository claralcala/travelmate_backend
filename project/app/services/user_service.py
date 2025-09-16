import base64
import os
import time
from io import BytesIO
from typing import Dict, Tuple, Union

from jinja2 import Template
from pydantic import EmailStr

from app import app_config
from app.modules.email_module import EmailModule
from app.modules.firebase_module import FirebaseModule
from app.repositories.user_repository import UserRepository
from app.schemas.login_schema import LoginOutputSchema
from app.schemas.refresh_token_schema import RefreshTokenOutputSchema
from app.schemas.user_schema import (
    UserEmailOutputSchema,
    UserInputSchema,
    UserOutputSchema,
)
from app.utils.security import generate_temporal_pwd
from app.utils.token_helper import decode_token, encode_token

from .user_service_exception import UserServiceException  # noqa: E501
from .user_service_exception import UserServiceExceptionInfo


class UserService:

    @staticmethod
    async def post_user(payload: UserInputSchema) -> UserEmailOutputSchema:
        user_photo = payload.photo
        payload.photo = None
        user_dict = payload.dict()



        if await UserRepository.email_exists(user_dict["email"]):
            raise UserServiceException(UserServiceExceptionInfo.EMAIL_IN_USE)
        if await UserRepository.nickname_exists(user_dict["nickname"]):
            raise UserServiceException(
                UserServiceExceptionInfo.NICKNAME_IN_USE
            )  # noqa: E501

        user = await UserRepository.create_user(user_dict)

    

        if user is None:
            raise UserServiceException(
                UserServiceExceptionInfo.FAILED_CREATE_USER
            )  # noqa: E501

        if user_photo:
            photo_data = base64.b64decode(user_photo)
            photo_io = BytesIO(photo_data)
            file_name = f"user_{user.id}.jpg"
            photo_response = FirebaseModule.upload_photo(
                photo_io, file_name, user.id
            )  # noqa: E501
            photo_url = photo_response.photo_url

            await UserRepository.update_user_profile_photo(user.id, photo_url)
            

        user_output = UserEmailOutputSchema(
            id=user.id,
            photo=user.photo,
            nickname=user.nickname,
            birthdate=user.birthdate,
            name=user.name,
            surname=user.surname,
            email=user.email,
            description=(
                user.description if "description" in user_dict else None
            ),  # noqa: E501
        )
        return user_output

    @staticmethod
    async def user_login(email: EmailStr, password: str) -> LoginOutputSchema:
        user_id = await UserRepository.user_login(email, password)

        if user_id is None:
            raise UserServiceException(UserServiceExceptionInfo.LOGIN_FAILED)

        # Generate user token
        token, expiration_timestamp = UserService._generate_token(
            user_id, app_config.token_expiration
        )
        # Generate refresh token
        refresh_token, r_exp_timestamp = UserService._generate_token(
            user_id, app_config.rt_expiration_time
        )

        # Save the token in the database
        await UserRepository.insert_token(user_id, token, refresh_token)

        return LoginOutputSchema(
            token=token,
            expire_token=expiration_timestamp,
            refresh_token=refresh_token,
            expire_refresh_token=r_exp_timestamp,
        )

    @staticmethod
    async def user_forgot_password(email: EmailStr) -> None:
        user_id = await UserRepository.get_user(email)
        if not user_id:
            return None
        temporal_pwd = generate_temporal_pwd()

        # updating the password in the database
        await UserRepository.update_password(user_id, temporal_pwd)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        template_file_path = os.path.join(dir_path, "mail_template.html")

        with open(template_file_path, "r") as file:
            template_str = file.read()

        jinja_template = Template(template_str)

        email_data = {
            "subject": "Contraseña temporal de Travel Mate",
            "greeting": f"¡Hola, {email}!",
            "message": (
                f"Tu contraseña temporal es: {temporal_pwd}. "
                "Recuerda cambiarla una vez la hayas usado "
                "para loguearte en la aplicación."
            ),
            "sender_name": "Travel Mate",
            "logo_url": "https://firebasestorage.googleapis.com/v0/b/fct24-89e51.appspot.com/o/logo.png?alt=media&token=1037491b-b6e1-4557-938a-14c75f8d1be1"
        }

        email_body = jinja_template.render(email_data)

        EmailModule.send_html_message(
            "travelmate.app24@gmail.com",
            email,
            "Contraseña temporal de Travel Mate",
            email_body,
        )

    @staticmethod
    def _generate_token(user_id: int, duration: int) -> Tuple[str, int]:
        """
        Create a new token with data passed in parameters
        :param user_id: user's id
        :param duration: duration of the generated token
        :return: generated token, expiration timestamp
        :rtype: Tuple[str, int]
        """
        # Calculate the date expiration of the token
        expiration_timestamp = int(round(time.time() + duration) * 1000)
        # Generate the token
        token = encode_token(
            {
                "user_id": user_id,
                "expiration_timestamp": expiration_timestamp,
            }
        )
        return token, expiration_timestamp

    @staticmethod
    async def is_valid_token(
        token: str, is_refresh_token: bool = False
    ) -> Union[Dict, None]:
        # Decodes token
        payload = decode_token(token)

        if payload and payload.get("expiration_timestamp") > time.time():

            return payload
        return None

    async def get_me(token: str, user_id: int) -> UserOutputSchema:
        me_response = await UserRepository.get_user_by_id(user_id)

        return UserOutputSchema(
            id=me_response.id,
            nickname=me_response.nickname,
            photo=me_response.photo,
            birthdate=me_response.birthdate,
            name=me_response.name,
            surname=me_response.surname,
            description=me_response.description,
        )

    async def logout_user(token: str) -> None:
        await UserRepository.logout_user(token)

    async def _refresh_token(
        token: str, is_refresh_token: bool, user_id: int = None
    ) -> Union[RefreshTokenOutputSchema, None]:
        token_payload = await UserService.is_valid_token(
            token, is_refresh_token=is_refresh_token
        )

        if token_payload:
            user_id = token_payload.get("user_id")

            # Generate new user token
            new_token, expiration_timestamp = UserService._generate_token(
                user_id, app_config.token_expiration
            )

            # Generate refresh token
            new_refresh_token, refresh_expiration_timestamp = (
                UserService._generate_token(
                    user_id, app_config.rt_expiration_time
                )  # noqa: E501
            )

            # update token in db
            await UserRepository.update_token(
                new_token,
                new_refresh_token,
                {
                    "user_id": user_id,
                    "refresh_token" if is_refresh_token else "token": token,
                },
            )

            return RefreshTokenOutputSchema(
                token=new_token,
                expire_token=expiration_timestamp,
                refresh_token=new_refresh_token,
                expire_refresh_token=refresh_expiration_timestamp,
            )

        return None

    async def refresh_user_token(
        refresh_token: str,
    ) -> RefreshTokenOutputSchema:  # noqa: E501
        token = await UserService._refresh_token(
            refresh_token, is_refresh_token=True
        )  # noqa: E501

        if token:
            return token
        else:
            raise UserServiceException(
                UserServiceExceptionInfo.INVALID_REFRESH_TOKEN
            )  # noqa: E501
