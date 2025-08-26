from fastapi import APIRouter, HTTPException, status

from bookings_study.api.dependencies import DBDep, UserIdDep
from bookings_study.api.exceptions import (
    DateFromBiggerOrEqualDateToHTTPException,
    RoomNotFoundHTTPException,
)
from bookings_study.services.bookings import BookingsService
from bookings_study.services.exceptions import (
    DateFromBiggerOrEqualDateToException,
    NoVacantRoomsException,
    RoomNotFoundException,
)
from bookings_study.schemas.bookings import (
    BookingsRequestSchema,
    BookingsSchema,
)


router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.get("", description="Get all bookings")
async def get_all_bookings(db: DBDep) -> list[BookingsSchema]:
    data = await BookingsService(db).get_bookings_all()
    return data


@router.get("/me", description="Get my bookings")
async def get_my_bookings(db: DBDep, user_id: UserIdDep) -> list[BookingsSchema]:
    data = await db.bookings.get_many_filtered(user_id=user_id)
    return data


@router.post("", status_code=201)
async def create_booking(
    db: DBDep, user_id: UserIdDep, request_data: BookingsRequestSchema
):
    try:
        data = await BookingsService(db).add_booking(
            user_id=user_id, request_data=request_data
        )
    except DateFromBiggerOrEqualDateToException:
        raise DateFromBiggerOrEqualDateToHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except NoVacantRoomsException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No vacant rooms remaining",
        )
    return {"status": "Ok", "data": data}
