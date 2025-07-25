from datetime import date
from typing import Annotated

from fastapi import APIRouter, Query, HTTPException, status
from fastapi_cache.decorator import cache

from src.repositories.exceptions import ForeignKeyException, NotFoundException
from src.api.dependencies import DBDep, PaginationDep
from src.api.exceptions import DateFromBiggerOrEqualDateToHTTPException
from src.schemas.hotels import HotelsSchema, HotelsPatchSchema, HotelsWriteSchema
from src.services.hotels import HotelService
from src.services.exceptions import DateFromBiggerOrEqualDateToException
router = APIRouter(prefix="/hotels", tags=["hotels"])


@router.get("")
@cache(expire=5)
async def get_hotels(
    db: DBDep,
    pagination: PaginationDep,
    date_from: date,
    date_to: date,
    title: Annotated[
        str | None, Query(description="Filter by substring hotel title")
    ] = None,
    location: Annotated[
        str | None, Query(description="Filter by substring hotel location")
    ] = None,
) -> list[HotelsSchema]:
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
    return data


@router.get("/{hotel_id}")
async def get_hotel(db: DBDep, hotel_id: int) -> HotelsSchema:
    try:
        data = await HotelService(db).get_hotel(hotel_id=hotel_id)
    except NotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
    return data


@router.post("", status_code=201)
async def create_hotel(db: DBDep, schema_create: HotelsWriteSchema):
    data = await HotelService(db).add_hotel(schema_create)
    return {"status": "Ok", "data": data}


@router.delete("/{hotel_id}", status_code=204)
async def delete_hotel(db: DBDep, hotel_id: int):
    try:
        await HotelService(db).delete_hotel(hotel_id=hotel_id)
    except NotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
    except ForeignKeyException:
        msg = "Cannot delete hotel that has rooms"
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=msg)
    return {"status": "Ok"}


@router.put("/{hotel_id}", status_code=204)
async def update_hotel(db: DBDep, hotel_id: int, schema_update: HotelsWriteSchema):
    try:
        await HotelService(db).edit_hotel(hotel_id=hotel_id, data=schema_update)
    except NotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
    return {"status": "Ok"}


@router.patch("/{hotel_id}", status_code=204)
async def patch_hotel(
    db: DBDep, hotel_id: int, schema_patch: HotelsPatchSchema
):
    try:
        await HotelService(db).edit_hotel_partially(hotel_id=hotel_id, data=schema_patch)
    except NotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
    return {"status": "Ok"}
