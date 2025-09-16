from app.schemas.app_schema import AppOutputSchema


class TransportationOutputSchema(AppOutputSchema):
    """
    Model to return a  transportation method response
    """

    id: int
    name: str
