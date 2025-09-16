import logging
from enum import Enum
from typing import Any, Optional, Union

from fastapi import HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class AppSchema(BaseModel):
    """
    Standard schema class of the application
    """

    pass


class AppOutputSchema(BaseModel):
    """
    Standard output model class of the application
    """

    def dict(self, *args, **kwargs):
        if kwargs and kwargs.get("exclude_none") is not None:
            kwargs["exclude_none"] = True
        return BaseModel.dict(self, *args, **kwargs)


class AppEmptyOutputSchema(AppOutputSchema):
    """
    Standard output model class of the application
    """

    pass


class AppErrorOutputSchema(AppOutputSchema):
    """
    Standard output model class of the application
    """

    code: int = 500
    error: Optional[Union[Any, None]] = None


class AppExceptionInfo(Enum):
    """
    Standard exception info of the app
    """

    def __init__(self, status_code: int, detail: str, http_code: int = 400):
        self.status_code = status_code
        self.detail = detail
        self.http_code = http_code

    def __str__(self):
        return self.detail


class AppException(HTTPException):
    def __init__(self, exception_info: AppExceptionInfo):
        super().__init__(
            status_code=exception_info.status_code,
            detail=exception_info.detail,  # noqa: E501
        )

        self.http_code = exception_info.http_code
