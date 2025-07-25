from fastapi import APIRouter, HTTPException, status

from src.api.dependencies import DBDep, UserIdDep
from src.api.exceptions import (
    DateFromBiggerOrEqualDateToHTTPException,
    RoomNotFoundHTTPException,
)
from src.services.bookings import BookingsService
from src.services.exceptions import (
    DateFromBiggerOrEqualDateToException,
    NoVacantRoomsException,
    RoomNotFoundException,
)
from src.schemas.bookings import (
    BookingsRequestSchema,
    BookingsSchema,
)


router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.get("")
async def get_all_bookings(db: DBDep) -> list[BookingsSchema]:
    data = await BookingsService(db).get_bookings_all()
    return data


@router.get("/me")
async def get_my_bookings(db: DBDep, user_id: UserIdDep) -> list[BookingsSchema]:
    data = await db.bookings.get_many_filtered(user_id=user_id)
    return data


@router.post("", status_code=201)
async def create_booking(
    db: DBDep, user_id: UserIdDep, request_data: BookingsRequestSchema
):
    try:
        data = await BookingsService(db).add_booking(user_id=user_id, request_data=request_data)
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
