from pydantic import EmailStr

from app.schemas.app_schema import AppSchema


class ForgotPasswordInputSchema(AppSchema):

    email: EmailStr
