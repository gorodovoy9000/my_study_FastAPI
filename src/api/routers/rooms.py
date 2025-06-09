from fastapi import APIRouter

from src.database import async_session_maker
from src.api.exceptions import only_one_error_handler, constrain_violation_error_handler
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomsSchema, RoomsPatchSchema, RoomsWriteSchema

# rooms linked to hotels
router = APIRouter(prefix="/hotels", tags=["HotelRooms"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int) -> list[RoomsSchema]:
    async with async_session_maker() as session:
        data = await RoomsRepository(session).get_rooms_by_hotel(hotel_id)
    return data


@router.get("/{hotel_id}/rooms/{room_id}")
@only_one_error_handler
async def get_room(hotel_id: int, room_id: int):
    # todo redundant hotel_id, when we have room_id which is primary_key
    async with async_session_maker() as session:
        data = await RoomsRepository(session).get_one(id=room_id)
    return data


@router.post("/{hotel_id/rooms", status_code=201)
@constrain_violation_error_handler
async def create_room(hotel_id: int, schema_create: RoomsWriteSchema):
    async with async_session_maker() as session:
        data = await RoomsRepository(session).add(schema_create)
        await session.commit()
    return {"status": "Ok", "data": data}


@router.delete("/{hotel_id}rooms/{room_id}", status_code=204)
@only_one_error_handler
@constrain_violation_error_handler
async def delete_room(hotel_id: int, room_id: int):
    # todo redundant hotel_id, when we have room_id which is primary_key
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id)
        await session.commit()
    return {"status": "Ok"}


@router.put("/{hotel_id}rooms/{room_id}", status_code=204)
@only_one_error_handler
@constrain_violation_error_handler
async def update_room(hotel_id: int, room_id: int, schema_update: RoomsWriteSchema):
    # todo redundant hotel_id, when we have room_id which is primary_key
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(schema_update, id=room_id)
        await session.commit()
    return {"status": "Ok"}


@router.patch("/{hotel_id}rooms/{room_id}", status_code=204)
@only_one_error_handler
@constrain_violation_error_handler
async def partial_update_room(hotel_id: int, room_id: int, schema_patch: RoomsPatchSchema):
    # todo redundant hotel_id, when we have room_id which is primary_key
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(schema_patch, partial_update=True, id=room_id)
        await session.commit()
    return {"status": "Ok"}
