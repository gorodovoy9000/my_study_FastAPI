from fastapi import APIRouter


from src.api.dependencies import DBDep, UserIdDep
from src.api.exceptions import only_one_error_handler
from src.schemas.bookings import BookingsRequestSchema, BookingsSchema, BookingsWriteSchema


router = APIRouter(prefix="/bookings", tags=["bookings"])


# @router.get("")
# async def get_bookings(db: DBDep):
#     pass
#
#
# @router.get("/{booking_id}")
# @only_one_error_handler
# async def get_booking(db: DBDep, booking_id: int) -> BookingsSchema:
#     pass


@router.post("", status_code=201)
async def create_booking(db: DBDep, user_id: UserIdDep, request_data: BookingsRequestSchema):
    # get room
    room = await db.rooms.get_one(id=request_data.room_id)
    # build booking add schema
    create_data = BookingsWriteSchema(
        room_id=room.id,
        user_id=user_id,
        date_from=request_data.date_from,
        date_to=request_data.date_to,
        price=room.price,
    )
    # execute
    data = await db.bookings.add(create_data)
    await db.commit()
    return {"status": "Ok", "data": data}
