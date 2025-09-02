from fastapi import APIRouter, Body, HTTPException, status

from bookings_study.api.v1.dependencies import DBDep, UserIdDep
from bookings_study.api.v1.exceptions import (
    BookingIsTooLongHTTPException,
    DateFromBiggerOrEqualDateToHTTPException,
    RoomNotFoundHTTPException,
)
from bookings_study.api.v1.examples import booking_examples
from bookings_study.services.bookings import BookingsService
from bookings_study.services.exceptions import (
    BookingIsTooLongException,
    DateFromBiggerOrEqualDateToException,
    NoVacantRoomsException,
    RoomNotFoundException,
)
from bookings_study.schemas.bookings import (
    BookingsRequestSchema,
    BookingsResponseSchema,
)


router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.get("", description="Get all bookings")
async def get_all_bookings(db: DBDep) -> BookingsResponseSchema:
    data = await BookingsService(db).get_bookings_all()
    return BookingsResponseSchema(data=data)


@router.get("/me", description="Get my bookings")
async def get_my_bookings(db: DBDep, user_id: UserIdDep) -> BookingsResponseSchema:
    data = await db.bookings.get_many_filtered(user_id=user_id)
    return BookingsResponseSchema(data=data)


@router.post("")
async def create_booking(
    db: DBDep,
    user_id: UserIdDep,
    request_data: BookingsRequestSchema = Body(openapi_examples=booking_examples),
) -> BookingsResponseSchema:
    try:
        data = await BookingsService(db).add_booking(
            user_id=user_id, request_data=request_data
        )
    except DateFromBiggerOrEqualDateToException:
        raise DateFromBiggerOrEqualDateToHTTPException
    except BookingIsTooLongException:
        raise BookingIsTooLongHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except NoVacantRoomsException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No vacant rooms remaining",
        )
    return BookingsResponseSchema(data=[data])
