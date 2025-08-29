from datetime import date
from typing import Annotated

from fastapi import APIRouter, Body, Query, HTTPException, status
from fastapi_cache.decorator import cache

from bookings_study.api.dependencies import DBDep, PaginationDep
from bookings_study.api.examples import start_date_examples, end_date_examples
from bookings_study.api.exceptions import (
    DateFromBiggerOrEqualDateToHTTPException,
    HotelNotFoundHTTPException,
)
from bookings_study.api.examples import hotels_examples
from bookings_study.schemas.base import BaseResponseSchema
from bookings_study.schemas.hotels import (
    HotelsPatchSchema,
    HotelsResponseSchema,
    HotelsWriteSchema,
)
from bookings_study.services.hotels import HotelService
from bookings_study.services.exceptions import (
    DateFromBiggerOrEqualDateToException,
    HotelNotFoundException,
    HotelHasRoomsException,
)

router = APIRouter(prefix="/hotels", tags=["hotels"])


@router.get("", description="Get vacant hotels by date interval")
@cache(expire=5)
async def get_hotels(
    db: DBDep,
    pagination: PaginationDep,
    date_from: Annotated[date, Query(openapi_examples=start_date_examples)],
    date_to: Annotated[date, Query(openapi_examples=end_date_examples)],
    title: Annotated[
        str | None, Query(description="Filter by substring hotel title")
    ] = None,
    location: Annotated[
        str | None, Query(description="Filter by substring hotel location")
    ] = None
) -> HotelsResponseSchema:
    try:
        data = await HotelService(db).get_hotels_filtered(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=pagination.limit,
            offset=pagination.offset,
        )
    except DateFromBiggerOrEqualDateToException:
        raise DateFromBiggerOrEqualDateToHTTPException
    return HotelsResponseSchema(data=data)


@router.get("/{hotel_id}")
async def get_hotel(db: DBDep, hotel_id: int) -> HotelsResponseSchema:
    try:
        data = await HotelService(db).get_hotel(hotel_id=hotel_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return HotelsResponseSchema(data=[data])


@router.post("")
async def create_hotel(db: DBDep, schema_create: HotelsWriteSchema = Body(openapi_examples=hotels_examples)) -> HotelsResponseSchema:
    data = await HotelService(db).add_hotel(schema_create)
    return HotelsResponseSchema(data=[data])


@router.delete("/{hotel_id}")
async def delete_hotel(db: DBDep, hotel_id: int) -> BaseResponseSchema:
    try:
        await HotelService(db).delete_hotel(hotel_id=hotel_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except HotelHasRoomsException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete hotel that has rooms",
        )
    return BaseResponseSchema()


@router.put("/{hotel_id}")
async def update_hotel(db: DBDep, hotel_id: int, schema_update: HotelsWriteSchema = Body(openapi_examples=hotels_examples)) -> BaseResponseSchema:
    try:
        await HotelService(db).edit_hotel(hotel_id=hotel_id, data=schema_update)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return BaseResponseSchema()


@router.patch("/{hotel_id}")
async def patch_hotel(db: DBDep, hotel_id: int, schema_patch: HotelsPatchSchema = Body(openapi_examples=hotels_examples)) -> BaseResponseSchema:
    try:
        await HotelService(db).edit_hotel_partially(
            hotel_id=hotel_id, data=schema_patch
        )
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return BaseResponseSchema()
