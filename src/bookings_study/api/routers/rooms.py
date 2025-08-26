from datetime import date, timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from bookings_study.services.exceptions import (
    DateFromBiggerOrEqualDateToException,
    FacilitiesInvalidException,
    HotelNotFoundException,
    RoomNotFoundException,
    RoomHasBookingsException,
)
from bookings_study.api.exceptions import (
    DateFromBiggerOrEqualDateToHTTPException,
    FacilitiesInvalidHTTPException,
    HotelNotFoundHTTPException,
    RoomNotFoundHTTPException,
)
from bookings_study.api.dependencies import DBDep
from bookings_study.schemas.rooms import (
    RoomsRequestPatchSchema,
    RoomsRequestPostSchema,
)
from bookings_study.schemas.relations import RoomsRelsSchema
from bookings_study.services.rooms import RoomService

# rooms linked to hotels
router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.get("")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: Annotated[date, Query(examples=[date.today()])],
    date_to: Annotated[date, Query(examples=[date.today() + timedelta(days=5)])],
) -> list[RoomsRelsSchema]:
    try:
        data = await RoomService(db).get_rooms_filtered(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )
    except DateFromBiggerOrEqualDateToException:
        raise DateFromBiggerOrEqualDateToHTTPException()
    return data


@router.post("", status_code=201)
async def create_room(db: DBDep, request_data: RoomsRequestPostSchema):
    try:
        data = await RoomService(db).add_room(request_data=request_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except FacilitiesInvalidException:
        raise FacilitiesInvalidHTTPException
    return {"status": "Ok", "data": data}


@router.get("/{room_id}")
async def get_room(db: DBDep, room_id: int) -> RoomsRelsSchema:
    try:
        data = await RoomService(db).get_room(room_id=room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return data


@router.delete("/{room_id}", status_code=204)
async def delete_room(db: DBDep, room_id: int):
    try:
        await RoomService(db).delete_room(room_id=room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except RoomHasBookingsException:
        msg = "Cannot delete room that has bookings"
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=msg)
    return {"status": "Ok"}


@router.put("/{room_id}", status_code=204)
async def update_room(
    db: DBDep, room_id: int, request_data: RoomsRequestPostSchema
):
    try:
        await RoomService(db).edit_room(room_id=room_id, request_data=request_data)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except HotelNotFoundHTTPException:
        raise HotelNotFoundHTTPException
    except FacilitiesInvalidHTTPException:
        raise FacilitiesInvalidHTTPException
    return {"status": "Ok"}


@router.patch("/{room_id}", status_code=204)
async def partial_update_room(
    db: DBDep, room_id: int, request_data: RoomsRequestPatchSchema
):
    try:
        await RoomService(db).edit_room_partially(
            room_id=room_id, request_data=request_data
        )
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except HotelNotFoundHTTPException:
        raise HotelNotFoundHTTPException
    except FacilitiesInvalidHTTPException:
        raise FacilitiesInvalidHTTPException
    return {"status": "Ok"}
