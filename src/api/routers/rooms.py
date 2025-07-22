from datetime import date

from fastapi import APIRouter, HTTPException, status

from src.exceptions import NotFoundException, ForeignKeyException
from src.api.dependencies import DBDep
from src.api.exceptions import validate_date_to_is_bigger_than_date_from
from src.schemas.rooms import (
    RoomsRequestPatchSchema,
    RoomsRequestPostSchema,
    RoomsPatchSchema,
    RoomsWriteSchema,
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
    validate_date_to_is_bigger_than_date_from(date_from=date_from, date_to=date_to)
    data = await db.rooms.get_vacant_rooms_by_hotel(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )
    return data


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(db: DBDep, hotel_id: int, room_id: int) -> RoomsRelsSchema:
    # todo redundant hotel_id, when we have room_id which is primary_key
    try:
        data = await db.rooms.get_one_with_rels(id=room_id)
    except NotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    return data


@router.post("/{hotel_id/rooms", status_code=201)
async def create_room(db: DBDep, hotel_id: int, schema_request: RoomsRequestPostSchema):
    # create room
    schema_create = RoomsWriteSchema(**schema_request.model_dump())
    try:
        data = await db.rooms.add(schema_create)
    except ForeignKeyException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
    # add facilities to room by their ids
    if schema_request.facilities_ids:
        try:
            await db.rooms.rooms_facilities_m2m.add(data.id, schema_request.facilities_ids)
        except ForeignKeyException:
            msg = "Some facilities are not found."
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=msg)
    await db.commit()
    return {"status": "Ok", "data": data}


@router.delete("/{hotel_id}rooms/{room_id}", status_code=204)
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    # todo redundant hotel_id, when we have room_id which is primary_key
    try:
        await db.rooms.delete(id=room_id)
    except NotFoundException:
        msg = "Room not found"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)
    except ForeignKeyException:
        msg = "Cannot delete room that has bookings"
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=msg)
    await db.commit()
    return {"status": "Ok"}


@router.put("/{hotel_id}rooms/{room_id}", status_code=204)
async def update_room(
    db: DBDep, hotel_id: int, room_id: int, schema_request: RoomsRequestPostSchema
):
    # todo redundant hotel_id, when we have room_id which is primary_key
    schema_update = RoomsWriteSchema(**schema_request.model_dump())
    try:
        await db.rooms.edit(schema_update, id=room_id)
    except NotFoundException:
        msg = "Room not found"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)
    except ForeignKeyException:
        msg = "Hotel not found"
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=msg)
    # change room facilities
    if schema_request.facilities_ids is not None:
        try:
            await db.rooms.rooms_facilities_m2m.edit(room_id, schema_request.facilities_ids)
        except ForeignKeyException:
            msg = "Some facilities are not found."
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=msg)
    await db.commit()
    return {"status": "Ok"}


@router.patch("/{hotel_id}rooms/{room_id}", status_code=204)
async def partial_update_room(
    db: DBDep, hotel_id: int, room_id: int, schema_request: RoomsRequestPatchSchema
):
    # todo redundant hotel_id, when we have room_id which is primary_key
    # partially update room
    data_patch = schema_request.model_dump(exclude_unset=True)
    if data_patch:
        schema_patch = RoomsPatchSchema(**data_patch)
        try:
            await db.rooms.edit(schema_patch, partial_update=True, id=room_id)
        except NotFoundException:
            msg = "Room not found"
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)
        except ForeignKeyException:
            msg = "Hotel not found"
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=msg)
    # change room facilities
    if schema_request.facilities_ids is not None:
        try:
            await db.rooms.rooms_facilities_m2m.edit(room_id, schema_request.facilities_ids)
        except ForeignKeyException:
            msg = "Some facilities are not found."
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=msg)
    await db.commit()
    return {"status": "Ok"}
