from app.repositories.city_repository import CityRepository
from app.repositories.trip_repository import TripRepository
from app.repositories.user_repository import UserRepository
from app.schemas.city_schema import CityOutputSchema
from app.schemas.pagination_schema import PaginationOutputSchema
from app.schemas.transportation_method_schema import TransportationOutputSchema
from app.schemas.trip_schema import (
    TripDetailOutputSchema,
    TripInputSchema,
    TripOutputSchema,
)
from app.schemas.user_schema import UserOutputSchema

from .trip_service_exception import TripServiceException  # noqa: E501
from .trip_service_exception import TripServiceExceptionInfo


class TripService:

    async def get_all_trips(
        page: int = 1, limit: int = 10
    ) -> PaginationOutputSchema[TripOutputSchema]:
        trips_info = await TripRepository.read_all_trips()
        # calculating starting and ending point for pagination
        start = (page - 1) * limit
        end = start + limit

        # list to save the results (initialized)
        trips_result_list = []

        for trip in trips_info:
            transportation = [
                TransportationOutputSchema(id=method.id, name=method.name)
                for method in trip.transportation_methods
            ]
            trip_schema = TripOutputSchema(
                id=trip.id,
                photo=trip.user.photo,
                origin=CityOutputSchema(
                    id=trip.origin.id,
                    name=trip.origin.name,
                    country=trip.origin.country,
                ),
                destination=CityOutputSchema(
                    id=trip.destination.id,
                    name=trip.destination.name,
                    country=trip.destination.country,
                ),
                start_date=trip.start_date,
                end_date=trip.end_date,
                description=trip.description,
                day_count=trip.day_count,
                number_of_participants=len(trip.participants) + 1,
                user_id=trip.user.id,
                transportation_methods=transportation,
            )
            trips_result_list.append(trip_schema)

        paginated_results = trips_result_list[start:end]
        total_records = len(trips_result_list)
        total_pages = (total_records + limit - 1) // limit
        return PaginationOutputSchema(
            page_number=page,
            page_size=limit,
            total_pages=total_pages,
            total_record=total_records,
            content=paginated_results,
        )

    async def get_trip(trip_id: int) -> TripDetailOutputSchema:

        trip = await TripRepository.read_trip(trip_id)

        if trip is None:
            raise TripServiceException(
                TripServiceExceptionInfo.TRIP_DOESNT_EXIST
            )  # noqa: E501

        transportation = [
            TransportationOutputSchema(id=method.id, name=method.name)
            for method in trip.transportation_methods
        ]
        participant_users = [
            UserOutputSchema(
                id=u.id,
                photo=u.photo,
                birthdate=u.birthdate,
                nickname=u.nickname,
                name=u.name,
                surname=u.surname,
                description=u.description,
            )
            for u in trip.participants
        ]

        trip_schema = TripDetailOutputSchema(
            id=trip.id,
            photo=trip.user.photo,
            origin=CityOutputSchema(
                id=trip.origin.id,
                name=trip.origin.name,
                country=trip.origin.country,  # noqa: E501
            ),
            destination=CityOutputSchema(
                id=trip.destination.id,
                name=trip.destination.name,
                country=trip.destination.country,
            ),
            start_date=trip.start_date,
            end_date=trip.end_date,
            description=trip.description,
            day_count=trip.day_count,
            creator=UserOutputSchema(
                id=trip.user.id,
                photo=trip.user.photo,
                birthdate=trip.user.birthdate,
                nickname=trip.user.nickname,
                name=trip.user.name,
                surname=trip.user.surname,
                description=trip.user.description,
            ),
            transportation_methods=transportation,
            participants=participant_users,
            number_of_participants=len(participant_users) + 1,
        )
        return trip_schema

    async def post_trip(
        payload: TripInputSchema, user_id: int
    ) -> TripOutputSchema:  # noqa: E501
        trip_dict = payload.dict()
        trip_dict["user_id"] = user_id
        trip_dict["origin"] = await CityRepository.read_city(payload.origin)
        trip_dict["destination"] = await CityRepository.read_city(
            payload.destination
        )  # noqa: E501
        delta = trip_dict["end_date"] - trip_dict["start_date"]
        trip_dict["day_count"] = delta.days
        trip = await TripRepository.create_trip(trip_dict)

        transportation_ids = trip_dict.get("transportation_method_ids", [])
        if not transportation_ids:
            raise TripServiceException(
                TripServiceExceptionInfo.NO_TRANSPORTATION_METHODS
            )
        transp_methods = await TripRepository.add_transportation_methods(
            trip, transportation_ids
        )
        if not transp_methods:
            raise TripServiceException(
                TripServiceExceptionInfo.NO_TRANSPORTATION_METHODS_WITH_ID
            )

        transp_schemas = [
            TransportationOutputSchema(id=method.id, name=method.name)
            for method in transp_methods
        ]
        trip_output = TripOutputSchema(
            id=trip.id,
            photo=trip.photo,
            origin=CityOutputSchema(
                id=trip.origin.id,
                name=trip.origin.name,
                country=trip.origin.country,  # noqa: E501
            ),
            destination=CityOutputSchema(
                id=trip.destination.id,
                name=trip.destination.name,
                country=trip.destination.country,
            ),
            start_date=trip.start_date,
            end_date=trip.end_date,
            description=trip.description,
            day_count=trip.day_count,
            user_id=user_id,
            transportation_methods=transp_schemas,
        )

        if trip_output is None:
            raise TripServiceException(
                TripServiceExceptionInfo.FAILED_CREATE_TRIP
            )  # noqa: E501
        return trip_output

    async def sign_up_for_trip(trip_id: int, user_id: int):
        trip = await TripRepository.read_trip(trip_id)
        if trip is None:
            raise TripServiceException(
                TripServiceExceptionInfo.TRIP_DOESNT_EXIST
            )  # noqa: E501
        user = await UserRepository.get_user_by_id(user_id)

        if (
            user in [participant for participant in trip.participants]
            or user == trip.user
        ):
            raise TripServiceException(
                TripServiceExceptionInfo.USER_ALREADY_SIGNED_FOR_TRIP
            )

        else:
            await TripRepository.add_participant(trip, user)

    async def resign_from_trip(trip_id: int, user_id: int):
        trip = await TripRepository.read_trip(trip_id)
        if trip is None:
            raise TripServiceException(
                TripServiceExceptionInfo.TRIP_DOESNT_EXIST
            )  # noqa: E501
        user = await UserRepository.get_user_by_id(user_id)

        if user in [participant for participant in trip.participants]:

            await TripRepository.delete_participant_from_trip(trip, user)

        else:
            raise TripServiceException(
                TripServiceExceptionInfo.USER_NOT_IN_PARTICIPANTS_LIST
            )

    async def delete_trip(trip_id: int, user_id: int):

        trip = await TripRepository.read_trip(trip_id)
        if trip is None:
            raise TripServiceException(
                TripServiceExceptionInfo.TRIP_DOESNT_EXIST
            )  # noqa: E501
        user = await UserRepository.get_user_by_id(user_id)

        if user == trip.user:
            await TripRepository.delete_trip(trip)

        else:
            raise TripServiceException(
                TripServiceExceptionInfo.USER_MUST_BE_CREATOR
            )  # noqa: E501
