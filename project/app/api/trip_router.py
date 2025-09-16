from typing import Any, Dict

from fastapi import APIRouter, Depends

from app.api import AuthBearer
from app.schemas.app_schema import AppEmptyOutputSchema
from app.schemas.pagination_schema import PaginationOutputSchema
from app.schemas.trip_schema import (
    TripDetailOutputSchema,
    TripInputSchema,
    TripOutputSchema,
)
from app.services.trip_service import TripService

router = APIRouter()


@router.get("", responses={200: {"model": TripOutputSchema}})
async def read_all_trips(
    page: int = 1, limit: int = 10
) -> PaginationOutputSchema[TripOutputSchema]:
    """method to get all trips"""
    all_trips = await TripService.get_all_trips(page, limit)

    return all_trips


@router.get(
    "/{trip_id}", response_model=TripDetailOutputSchema, status_code=200
)  # noqa: E501
async def read_trip(trip_id: int) -> TripDetailOutputSchema:
    """method to get specific trip by id"""
    trip = await TripService.get_trip(trip_id)

    return trip


@router.post("/create", responses={200: {"model": TripOutputSchema}})
async def create_trip(
    payload: TripInputSchema, user_info: Dict[str, Any] = Depends(AuthBearer())
) -> TripOutputSchema:
    """
    method to create a new trip
    args: trip_info, user_info
    return: TripOutputSchema
    """
    # Getting the id from the info collected from the token
    user_id = user_info["user_id"]

    return await TripService.post_trip(payload, user_id)


@router.post(
    "/{trip_id}/joinTrip", responses={200: {"model": AppEmptyOutputSchema}}
)  # noqa: E501
async def join_trip(
    trip_id: int, user_info: Dict[str, Any] = Depends(AuthBearer())
) -> AppEmptyOutputSchema:

    user_id = user_info["user_id"]

    await TripService.sign_up_for_trip(trip_id, user_id)

    return AppEmptyOutputSchema


@router.delete(
    "/{trip_id}/unjoinTrip", responses={200: {"model": AppEmptyOutputSchema}}
)
async def unjoin_trip(
    trip_id: int, user_info: Dict[str, Any] = Depends(AuthBearer())
) -> AppEmptyOutputSchema:

    user_id = user_info["user_id"]

    await TripService.resign_from_trip(trip_id, user_id)
    return AppEmptyOutputSchema


@router.delete(
    "/{trip_id}/deleteTrip", responses={200: {"model": AppEmptyOutputSchema}}
)
async def delete_trip(
    trip_id: int, user_info: Dict[str, Any] = Depends(AuthBearer())
) -> AppEmptyOutputSchema:
    user_id = user_info["user_id"]

    await TripService.delete_trip(trip_id, user_id)
    return AppEmptyOutputSchema
