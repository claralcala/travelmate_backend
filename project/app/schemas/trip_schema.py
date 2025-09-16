from datetime import date, datetime
from typing import List, Optional

from pydantic import validator

from app.schemas.app_schema import AppOutputSchema, AppSchema
from app.schemas.city_schema import CityOutputSchema
from app.schemas.transportation_method_schema import TransportationOutputSchema
from app.schemas.user_schema import UserOutputSchema


class TripBaseOutputSchema(AppOutputSchema):
    """
    Schema to return a trip - with the common atributes
    json_encoders --
    to get the date in an appropiate european format, dd-mm-yyyy
    """

    id: int
    photo: Optional[str] = None
    origin: CityOutputSchema
    destination: CityOutputSchema
    start_date: date
    end_date: date
    description: Optional[str] = None
    day_count: int
    number_of_participants: Optional[int] = None
    transportation_methods: List[TransportationOutputSchema] = []

    class Config:
        json_encoders = {
            date: lambda v: v.strftime("%d-%m-%Y"),
        }


class TripOutputSchema(TripBaseOutputSchema):
    """
    Schema to return a trip
    for the trips list
    """

    user_id: int


class TripDetailOutputSchema(TripBaseOutputSchema):
    """
    Schema to return a trip
    for the trip details
    """

    creator: Optional[UserOutputSchema] = None
    participants: List[UserOutputSchema] = []


class TripInputSchema(AppSchema):
    """
    Schema to create/update a trip
    """

    photo: Optional[str] = None
    origin: int
    destination: int
    start_date: date
    end_date: date
    description: Optional[str]
    transportation_method_ids: List[int] = []

    @validator("start_date", "end_date", pre=True)
    def parse_date(cls, value: str) -> datetime:
        try:
            return datetime.strptime(value, "%d-%m-%Y").date()
        except ValueError:

            raise ValueError("Incorrect date, format must be dd-mm-yyyy")

    @validator("start_date")
    def validate_start_date(cls, start_date):
        if start_date < date.today():
            raise ValueError("Start date can't be in the past")
        return start_date

    @validator("end_date")
    def validate_end_date(cls, end_date, values, **kwargs):
        start_date = values.get("start_date")
        if start_date and end_date < start_date:
            raise ValueError("End date can't be before start date")
        return end_date
