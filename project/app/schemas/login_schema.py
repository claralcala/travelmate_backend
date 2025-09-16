from pydantic import EmailStr

from app.schemas.app_schema import AppOutputSchema, AppSchema


class LoginInputSchema(AppSchema):

    email: EmailStr
    password: str


class LoginOutputSchema(AppOutputSchema):
    """
    Model to return a token response
    """

    token: str
    expire_token: int
    refresh_token: str
    expire_refresh_token: int
