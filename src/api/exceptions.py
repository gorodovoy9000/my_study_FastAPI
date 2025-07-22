import functools

from fastapi import HTTPException
from starlette import status

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
