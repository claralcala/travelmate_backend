from app.schemas.app_schema import AppException, AppExceptionInfo


class TripServiceExceptionInfo(AppExceptionInfo):
    FAILED_CREATE_TRIP = (
        1001,
        "Failed to create trip",
    )
    NO_TRANSPORTATION_METHODS_WITH_ID = (
        1002,
        "No transportation methods found with the provided ids",
    )
    NO_TRANSPORTATION_METHODS = (
        1003,
        "No transportation methods provided",
    )
    USER_ALREADY_SIGNED_FOR_TRIP = (
        1004,
        "User already signed up for that trip",
    )  # noqa: E501
    TRIP_DOESNT_EXIST = (
        1005,
        "A trip with that id doesn't exist",
    )
    USER_NOT_IN_PARTICIPANTS_LIST = (
        1006,
        "The user is not in this trip's participant list",
    )
    USER_MUST_BE_CREATOR = (
        1007,
        "User must be the creator of the trip to delete it",
    )  # noqa: E501



class TripServiceException(AppException):
    """
    Class that define a trip service exception
    """

    pass
