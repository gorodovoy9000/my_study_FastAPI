from datetime import date

from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.api.exceptions import only_one_error_handler, constrain_violation_error_handler
from src.schemas.rooms import (
    RoomsRequestPatchSchema, RoomsRequestPostSchema,
    RoomsPatchSchema, RoomsWriteSchema,
)
from src.schemas.relations import RoomsRelsSchema

# rooms linked to hotels
router = APIRouter(prefix="/hotels", tags=["HotelRooms"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        db: DBDep,
        hotel_id: int,
        date_from: date,
        date_to: date,
) -> list[RoomsRelsSchema]:
    data = await db.rooms.get_vacant_rooms_by_hotel(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
    return data


@router.get("/{hotel_id}/rooms/{room_id}")
@only_one_error_handler
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    # todo redundant hotel_id, when we have room_id which is primary_key
    data = await db.rooms.get_one(id=room_id)
    return data


@router.post("/{hotel_id/rooms", status_code=201)
@constrain_violation_error_handler
async def create_room(db: DBDep, hotel_id: int, schema_request: RoomsRequestPostSchema):
    # create room
    schema_create = RoomsWriteSchema(**schema_request.model_dump())
    data = await db.rooms.add(schema_create)
    # add facilities to room by their ids
    if schema_request.facilities_ids:
        await db.rooms.rooms_facilities_m2m.add(data.id, schema_request.facilities_ids)
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
async def update_room(db: DBDep, hotel_id: int, room_id: int, schema_request: RoomsRequestPostSchema):
    # todo redundant hotel_id, when we have room_id which is primary_key
    schema_update = RoomsWriteSchema(**schema_request.model_dump())
    await db.rooms.edit(schema_update, id=room_id)
    # change room facilities
    if schema_request.facilities_ids is not None:
        await db.rooms.rooms_facilities_m2m.edit(room_id, schema_request.facilities_ids)
    await db.commit()
    return {"status": "Ok"}


@router.patch("/{hotel_id}rooms/{room_id}", status_code=204)
@only_one_error_handler
@constrain_violation_error_handler
async def partial_update_room(db: DBDep, hotel_id: int, room_id: int, schema_request: RoomsRequestPatchSchema):
    # todo redundant hotel_id, when we have room_id which is primary_key
    # partially update room
    data_patch = schema_request.model_dump(exclude_unset=True)
    if data_patch:
        schema_patch = RoomsPatchSchema(**data_patch)
        await db.rooms.edit(schema_patch, partial_update=True, id=room_id)
    # change room facilities
    if schema_request.facilities_ids is not None:
        await db.rooms.rooms_facilities_m2m.edit(room_id, schema_request.facilities_ids)
    await db.commit()
    return {"status": "Ok"}
