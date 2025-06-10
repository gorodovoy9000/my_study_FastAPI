from typing import Annotated

from fastapi import APIRouter, Query

from src.api.dependencies import DBDep, PaginationDep
from src.api.exceptions import only_one_error_handler
from src.schemas.hotels import HotelsSchema, HotelsPatchSchema, HotelsWriteSchema

router = APIRouter(prefix="/hotels", tags=["hotels"])


@router.get("")
async def get_hotels(
        db: DBDep,
        pagination: PaginationDep,
        title: Annotated[str | None, Query(description="Filter by substring hotel title")] = None,
        location: Annotated[str | None, Query(description="Filter by substring hotel location")] = None,
) -> list[HotelsSchema]:
    data = await db.hotels.get_all(
        location=location,
        title=title,
        limit=pagination.limit,
        offset=pagination.offset,
    )
    return data


@router.get("/{hotel_id}")
@only_one_error_handler
async def get_hotel(db: DBDep, hotel_id: int) -> HotelsSchema:
    data = await db.hotels.get_one(id=hotel_id)
    return data


@router.post("", status_code=201)
async def create_hotel(db: DBDep, schema_create: HotelsWriteSchema):
    data = await db.hotels.add(schema_create)
    # transaction commit MUST stay here!
    await db.commit()
    return {"status": "Ok", "data": data}


@router.delete("/{hotel_id}", status_code=204)
@only_one_error_handler
async def delete_hotel(db: DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "Ok"}


@router.put("/{hotel_id}", status_code=204)
@only_one_error_handler
async def update_hotel(db: DBDep, hotel_id: int, schema_update: HotelsWriteSchema):
    await db.hotels.edit(schema_update, id=hotel_id)
    await db.commit()
    return {"status": "Ok"}


@router.patch("/{hotel_id}", status_code=204)
@only_one_error_handler
async def partial_update_hotel(db: DBDep, hotel_id: int, schema_patch: HotelsPatchSchema):
    await db.hotels.edit(schema_patch, partial_update=True, id=hotel_id)
    await db.commit()
    return {"status": "Ok"}
