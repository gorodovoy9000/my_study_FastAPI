from datetime import date
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


# def constrain_violation_error_handler(func):
#     @functools.wraps(func)
#     async def wrapper(*args, **kwargs):
#         try:
#             return await func(*args, **kwargs)
#         except ForeignKeyException as err:
#             raise HTTPException(
#                 status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#                 detail=str(err),
#             )
#         except NullValueException as err:
#             raise HTTPException(
#                 status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#                 detail=str(err),
#             )
#         except UniqueValueException as err:
#             raise HTTPException(
#                 status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#                 detail=str(err),
#             )
#
#     return wrapper


def validate_date_to_is_bigger_than_date_from(date_from: date, date_to: date):
    if date_from >= date_to:
        msg = "date_to must be bigger than date_from"
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=msg)
