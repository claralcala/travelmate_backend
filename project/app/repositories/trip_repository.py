from datetime import date
from typing import Any, Dict, List
from tortoise.exceptions import DoesNotExist
from app.modules.database_module.models import Trip, User
from app.modules.database_module.models.transportation_method_model import (
    TransportationMethod,
)
from app.repositories.app_repository import AppRepository


class TripRepository(AppRepository):

    @staticmethod
    async def read_all_trips() -> List[Trip]:
        """
        Method to get all trips
        """

        today = date.today()
        trips_info = (
            await Trip.filter(start_date__gte=today)
            .prefetch_related(
                "user",
                "origin",
                "destination",
                "transportation_methods",
                "participants",
            )
            .order_by("start_date")
        )

        return trips_info

    @staticmethod
    async def read_trip(trip_id: int) -> Trip:
        """
        Method to get specific trip by its id
        """
        try:
            trip = await Trip.get(id=trip_id).prefetch_related(
                "user",
                "origin",
                "destination",
                "transportation_methods",
                "participants",  # noqa: E501
            )
            return trip
        except DoesNotExist:
            return None
        
    @staticmethod
    async def create_trip(trip_info: Dict[str, Any]) -> Trip:
        """
        Method to create a new trip
        """

        trip = await Trip.create(**trip_info)

        return trip

    @staticmethod
    async def add_transportation_methods(
        trip: Trip, method_ids: List[int]
    ) -> List[TransportationMethod]:
        """
        Method to add the transportation list
        to the intermediate table
        """
        if method_ids:
            transp_methods = await TransportationMethod.filter(
                id__in=method_ids
            ).all()  # noqa: E501
            await trip.transportation_methods.add(*transp_methods)
            return transp_methods
        # in the case the list is empty, the method returns it like that
        return []

    @staticmethod
    async def add_participant(trip: Trip, user: User):
        """
        Method that adds a participant to a trip
        """

        await trip.participants.add(user)

    @staticmethod
    async def delete_participant_from_trip(trip: Trip, user: User):
        """
        Method that deletes a participant from a trip

        """

        await trip.participants.remove(user)

    @staticmethod
    async def delete_trip(trip: Trip):
        """
        Method that deletes specific trip
        """

        await Trip.delete(trip)
