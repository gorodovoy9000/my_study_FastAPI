from fastapi import APIRouter, HTTPException, status

from src.api.dependencies import DBDep, UserIdDep
from src.api.exceptions import validate_date_to_is_bigger_than_date_from
from src.exceptions import NotFoundException, NoVacantRoomsException
from src.schemas.bookings import (
    BookingsRequestSchema,
    BookingsSchema,
    BookingsWriteSchema,
)


router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.get("")
async def get_all_bookings(db: DBDep) -> list[BookingsSchema]:
    data = await db.bookings.get_all()
    return data


@router.get("/me")
async def get_my_bookings(db: DBDep, user_id: UserIdDep) -> list[BookingsSchema]:
    data = await db.bookings.get_many_filtered(user_id=user_id)
    return data


@router.post("", status_code=201)
async def create_booking(
    db: DBDep, user_id: UserIdDep, request_data: BookingsRequestSchema
):
    validate_date_to_is_bigger_than_date_from(date_from=request_data.date_from, date_to=request_data.date_to)
    # get room
    try:
        room = await db.rooms.get_one(id=request_data.room_id)
    except NotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    # build booking add schema
    create_data = BookingsWriteSchema(
        user_id=user_id, price=room.price, **request_data.model_dump()
    )
    # execute
    try:
        data = await db.bookings.add_booking(create_data)
    except NoVacantRoomsException as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=err.detail)
    await db.commit()
    return {"status": "Ok", "data": data}
