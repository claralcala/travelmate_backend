from app.schemas.app_schema import AppOutputSchema


class PhotoOutputSchema(AppOutputSchema):
    photo_url: str
