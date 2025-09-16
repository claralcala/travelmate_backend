from app.schemas.app_schema import AppException, AppExceptionInfo


class UserServiceExceptionInfo(AppExceptionInfo):
    EMAIL_IN_USE = 402, "Email already in use"
    NICKNAME_IN_USE = 405, "Nickname already in use"
    FAILED_CREATE_USER = 406, "Failed to create user", 500
    INVALID_USER = 407, "User not found"
    INCORRECT_PASSWORD = 408, "Incorrect password"
    INVALID_AUTHENTICATION_SCHEME = 409, "Invalid authentication scheme"
    INVALID_AUTHENTICATION_TOKEN = 409, "Invalid or expired token"
    LOGIN_FAILED = 410, "Login failed"
    EMPTY_RESPONSE = 411, ""
    INVALID_REFRESH_TOKEN = 412, "The refresh token provided is not valid"


class UserServiceException(AppException):
    """
    Class that define a user service exception
    """

    pass
