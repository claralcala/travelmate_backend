from app.schemas.app_schema import AppOutputSchema


class CityOutputSchema(AppOutputSchema):
    """
    Model to return a city response
    """

    id: int
    name: str
    country: str
