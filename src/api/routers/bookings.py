from fastapi import APIRouter, HTTPException, status


from src.api.dependencies import DBDep, UserIdDep
from src.api.exceptions import only_one_error_handler
from src.exceptions import NoVacantRoomsException
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
@only_one_error_handler
async def get_my_bookings(db: DBDep, user_id: UserIdDep) -> list[BookingsSchema]:
    data = await db.bookings.get_many_filtered(user_id=user_id)
    return data


@router.post("", status_code=201)
async def create_booking(
    db: DBDep, user_id: UserIdDep, request_data: BookingsRequestSchema
):
    # get room
    room = await db.rooms.get_one(id=request_data.room_id)
    # build booking add schema
    create_data = BookingsWriteSchema(
        user_id=user_id, price=room.price, **request_data.model_dump()
    )
    # execute
    try:
        data = await db.bookings.add_booking(create_data)
    except NoVacantRoomsException as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    await db.commit()
    return {"status": "Ok", "data": data}
