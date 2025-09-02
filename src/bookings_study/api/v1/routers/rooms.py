from datetime import date
from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Query, status

from bookings_study.services.exceptions import (
    DateFromBiggerOrEqualDateToException,
    FacilitiesInvalidException,
    HotelNotFoundException,
    RoomAlreadyExistsException,
    RoomNotFoundException,
    RoomHasBookingsException,
)
from bookings_study.api.v1.examples import (
    start_date_examples,
    end_date_examples,
    rooms_examples,
)
from bookings_study.api.v1.exceptions import (
    DateFromBiggerOrEqualDateToHTTPException,
    FacilitiesInvalidHTTPException,
    HotelNotFoundHTTPException,
    RoomAlreadyExistsHTTPException,
    RoomNotFoundHTTPException,
)
from bookings_study.api.v1.dependencies import DBDep
from bookings_study.schemas.base import BaseResponseSchema
from bookings_study.schemas.rooms import (
    RoomsRequestPatchSchema,
    RoomsRequestPostSchema,
    RoomsResponseSchema,
)
from bookings_study.schemas.relations import RoomsResponseRelsSchema
from bookings_study.services.rooms import RoomService

# rooms linked to hotels
router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.get("", description="Get vacant rooms by hotel and date interval")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: Annotated[date, Query(openapi_examples=start_date_examples)],
    date_to: Annotated[date, Query(openapi_examples=end_date_examples)],
) -> RoomsResponseRelsSchema:
    try:
        data = await RoomService(db).get_rooms_filtered(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )
    except DateFromBiggerOrEqualDateToException:
        raise DateFromBiggerOrEqualDateToHTTPException()
    return RoomsResponseRelsSchema(data=data)


@router.post("")
async def create_room(
    db: DBDep,
    request_data: RoomsRequestPostSchema = Body(openapi_examples=rooms_examples),
) -> RoomsResponseSchema:
    try:
        data = await RoomService(db).add_room(request_data=request_data)
    except RoomAlreadyExistsException:
        raise RoomAlreadyExistsHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except FacilitiesInvalidException:
        raise FacilitiesInvalidHTTPException
    return RoomsResponseSchema(data=[data])


@router.get("/{room_id}")
async def get_room(db: DBDep, room_id: int) -> RoomsResponseRelsSchema:
    try:
        data = await RoomService(db).get_room(room_id=room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return RoomsResponseRelsSchema(data=[data])


@router.delete("/{room_id}")
async def delete_room(db: DBDep, room_id: int) -> BaseResponseSchema:
    try:
        await RoomService(db).delete_room(room_id=room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except RoomHasBookingsException:
        msg = "Cannot delete room that has bookings"
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=msg)
    return BaseResponseSchema()


@router.put("/{room_id}")
async def update_room(
    db: DBDep,
    room_id: int,
    request_data: RoomsRequestPostSchema = Body(openapi_examples=rooms_examples),
) -> BaseResponseSchema:
    try:
        await RoomService(db).edit_room(room_id=room_id, request_data=request_data)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except RoomAlreadyExistsException:
        raise RoomAlreadyExistsHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except FacilitiesInvalidException:
        raise FacilitiesInvalidHTTPException
    return BaseResponseSchema()


@router.patch("/{room_id}")
async def partial_update_room(
    db: DBDep,
    room_id: int,
    request_data: RoomsRequestPatchSchema = Body(openapi_examples=rooms_examples),
) -> BaseResponseSchema:
    try:
        await RoomService(db).edit_room_partially(
            room_id=room_id, request_data=request_data
        )
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except RoomAlreadyExistsException:
        raise RoomAlreadyExistsHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except FacilitiesInvalidException:
        raise FacilitiesInvalidHTTPException
    return BaseResponseSchema()
