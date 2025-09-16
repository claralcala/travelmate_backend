import re
from datetime import date, datetime
from typing import Optional

from pydantic import EmailStr, Field, validator

from app.schemas.app_schema import AppOutputSchema, AppSchema


class UserOutputSchema(AppOutputSchema):
    """
    Schema to return a user
    json_encoders --
    converter to return dates in an appropiate european format dd-mm-yyyy
    """

    id: int
    photo: Optional[str] = None
    nickname: str
    photo: Optional[str] = None
    birthdate: date
    name: str
    surname: Optional[str]
    description: Optional[str] = None

    class Config:
        json_encoders = {
            date: lambda v: v.strftime("%d-%m-%Y"),
        }


class UserEmailOutputSchema(UserOutputSchema):

    email: EmailStr


class UserInputSchema(AppSchema):
    """
    Schema to create/update a user
    validate_password --
    method that checks that the password meets certain conditions
    parse_birthdate --
    method that parses de dato to an appropiate european format dd-mm-yyyy
    """

    photo: Optional[str] = None
    nickname: str
    password: str
    email: EmailStr
    birthdate: date
    name: str
    surname: Optional[str]
    description: Optional[str] = None

    @validator("password")
    def validate_password(cls, value):
        if (
            len(value) < 8
            or not re.search("[a-z]", value)
            or not re.search("[A-Z]", value)
            or not re.search('[!@#$%^&*(),.?":{}|<>]', value)
        ):
            raise ValueError(
                "Password must have at least 8 characters, "
                "include 1 lowercase letter, "
                "1 uppercase letter and 1 non alphanumeric character"
            )
        return value

    @validator("birthdate", pre=True)
    def parse_birthdate(cls, value: str) -> date:
        try:
            # Converting date to specified format
            birth_date = datetime.strptime(value, "%d-%m-%Y").date()
        except ValueError:
            # Raising exception in case of incorrect date
            raise ValueError("Incorrect date, format must be dd-mm-yyyy")

        # Check if the user is at least 18 years old
        current_date = date.today()
        user_age = (
            current_date.year
            - birth_date.year
            - (
                (current_date.month, current_date.day)
                < (birth_date.month, birth_date.day)
            )
        )

        if user_age < 18:
            raise ValueError(
                "You must be at least 18 to sign up in Travel Mate"
            )  # noqa: E501
        return birth_date
