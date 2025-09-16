from app.schemas.app_schema import AppOutputSchema, AppSchema


class RefreshTokenOutputSchema(AppOutputSchema):
    """
    Model to return a token response
    """

    token: str
    expire_token: int
    refresh_token: str
    expire_refresh_token: int


class RefreshTokenInputSchema(AppSchema):

    refresh_token: str
