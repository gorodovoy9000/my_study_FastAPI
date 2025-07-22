from datetime import date
from typing import Annotated

from fastapi import APIRouter, Query, HTTPException, status
from fastapi_cache.decorator import cache

from src.exceptions import ForeignKeyException, NotFoundException
from src.api.dependencies import DBDep, PaginationDep
from src.schemas.hotels import HotelsSchema, HotelsPatchSchema, HotelsWriteSchema

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
    if date_from >= date_to:
        msg = "DateTo must be lesser than DateFrom"
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=msg)
    data = await db.hotels.get_hotels_with_vacant_rooms(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        limit=pagination.limit,
        offset=pagination.offset,
    )
    return data


@router.get("/{hotel_id}")
async def get_hotel(db: DBDep, hotel_id: int) -> HotelsSchema:
    try:
        data = await db.hotels.get_one(id=hotel_id)
    except NotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
    return data


@router.post("", status_code=201)
async def create_hotel(db: DBDep, schema_create: HotelsWriteSchema):
    data = await db.hotels.add(schema_create)
    # transaction commit MUST stay here!
    await db.commit()
    return {"status": "Ok", "data": data}


@router.delete("/{hotel_id}", status_code=204)
async def delete_hotel(db: DBDep, hotel_id: int):
    try:
        await db.hotels.delete(id=hotel_id)
    except NotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
    except ForeignKeyException:
        msg = "Cannot delete hotel that has rooms"
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=msg)
    await db.commit()
    return {"status": "Ok"}


@router.put("/{hotel_id}", status_code=204)
async def update_hotel(db: DBDep, hotel_id: int, schema_update: HotelsWriteSchema):
    try:
        await db.hotels.edit(schema_update, id=hotel_id)
    except NotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
    await db.commit()
    return {"status": "Ok"}


@router.patch("/{hotel_id}", status_code=204)
async def partial_update_hotel(
    db: DBDep, hotel_id: int, schema_patch: HotelsPatchSchema
):
    try:
        await db.hotels.edit(schema_patch, partial_update=True, id=hotel_id)
    except NotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
    await db.commit()
    return {"status": "Ok"}
