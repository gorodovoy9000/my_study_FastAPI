# from datetime import date
import functools

from fastapi import HTTPException, status

from src.exceptions import (
    ForeignKeyException,
    ManyFoundException,
    NullValueException,
    NotFoundException,
    UniqueValueException,
)


def only_one_error_handler(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except NotFoundException:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Object not found",
            )
        except ManyFoundException:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Multiple objects found, only one allowed",
            )

    return wrapper


class AppBaseHTTPException(HTTPException):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    details: str = ""

    def __init__(self):
        super().__init__(
            status_code=self.status_code,
            detail=self.details,
        )


class DateFromBiggerOrEqualDateToHTTPException(AppBaseHTTPException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "date_to must be bigger than date_from"
