from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.api.exceptions import only_one_error_handler, constrain_violation_error_handler
from src.schemas.rooms import RoomsSchema, RoomsPatchSchema, RoomsWriteSchema

# rooms linked to hotels
router = APIRouter(prefix="/hotels", tags=["HotelRooms"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(db: DBDep, hotel_id: int) -> list[RoomsSchema]:
    data = await db.rooms.get_many_filtered(hotel_id=hotel_id)
    return data


@router.get("/{hotel_id}/rooms/{room_id}")
@only_one_error_handler
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    # todo redundant hotel_id, when we have room_id which is primary_key
    data = await db.rooms.get_one(id=room_id)
    return data


@router.post("/{hotel_id/rooms", status_code=201)
@constrain_violation_error_handler
async def create_room(db: DBDep, hotel_id: int, schema_create: RoomsWriteSchema):
    data = await db.rooms.add(schema_create)
    await db.commit()
    return {"status": "Ok", "data": data}


@router.delete("/{hotel_id}rooms/{room_id}", status_code=204)
@only_one_error_handler
@constrain_violation_error_handler
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    # todo redundant hotel_id, when we have room_id which is primary_key
    await db.rooms.delete(id=room_id)
    await db.commit()
    return {"status": "Ok"}


@router.put("/{hotel_id}rooms/{room_id}", status_code=204)
@only_one_error_handler
@constrain_violation_error_handler
async def update_room(db: DBDep, hotel_id: int, room_id: int, schema_update: RoomsWriteSchema):
    # todo redundant hotel_id, when we have room_id which is primary_key
    await db.rooms.edit(schema_update, id=room_id)
    await db.commit()
    return {"status": "Ok"}


@router.patch("/{hotel_id}rooms/{room_id}", status_code=204)
@only_one_error_handler
@constrain_violation_error_handler
async def partial_update_room(db: DBDep, hotel_id: int, room_id: int, schema_patch: RoomsPatchSchema):
    # todo redundant hotel_id, when we have room_id which is primary_key
    await db.rooms.edit(schema_patch, partial_update=True, id=room_id)
    await db.commit()
    return {"status": "Ok"}
