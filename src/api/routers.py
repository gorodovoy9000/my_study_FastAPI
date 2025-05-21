from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import insert, select, delete

from repositories.hotels import HotelsRepository
from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models import HotelsOrm
from src.schemas import HotelScheme, HotelWriteScheme, HotelPatchScheme

router = APIRouter(prefix="/hotels", tags=["hotels"])


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        title: Annotated[str | None, Query(description="Filter by substring hotel title")] = None,
        location: Annotated[str | None, Query(description="Filter by substring hotel location")] = None,
) -> list[HotelScheme]:
    async with async_session_maker() as session:
        items_orm = await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=pagination.per_page,
            offset=pagination.per_page * (pagination.page - 1),
        )
    return [HotelScheme.model_validate(mo, from_attributes=True) for mo in items_orm]


@router.delete("/{hotel_id}", status_code=204)
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        stmt = (
            delete(HotelsOrm)
            .where(HotelsOrm.id == hotel_id)
            .returning(HotelsOrm.id)
        )
        result = await session.execute(stmt)
        deleted_item_id = result.scalars().first()
        # debug deleted item id print
        print(deleted_item_id)
        await session.commit()
    return {"status": "Ok"}


@router.post("", status_code=201)
async def create_hotel(scheme_create: HotelWriteScheme):
    async with async_session_maker() as session:
        item_orm = await HotelsRepository(session).add(**scheme_create.model_dump())
        # transaction commit MUST stay here!
        await session.commit()
    return {"status": "Ok", "data": item_orm}


# @router.put("/{hotel_id}", status_code=204)
# async def update_hotel(
#         hotel_id: int,
#         hotel_scheme: HotelPatchScheme,
# ):
#     # get hotel
#     list_index_hotel = None
#     for i, hotel in enumerate(hotels_db):
#         if hotel["id"] == hotel_id:
#             list_index_hotel = i
#     # not found by id
#     if list_index_hotel is None:
#         raise HTTPException(status_code=404, detail="Hotel not found")
#     # replace hotel data
#     hotels_db[list_index_hotel] = {"id": hotel_id, "name": hotel_scheme.name, "title": hotel_scheme.title}
#     return {"status": "Ok"}
#
#
# @router.patch("/{hotel_id}", status_code=204)
# async def update_hotel(
#         hotel_id: int,
#         hotel_scheme: HotelPatchScheme,
# ):
#     # get hotel
#     list_index_hotel = None
#     for i, hotel in enumerate(hotels_db):
#         if hotel["id"] == hotel_id:
#             list_index_hotel = i
#     # not found by id
#     if list_index_hotel is None:
#         raise HTTPException(status_code=404, detail="Hotel not found")
#     # partial update
#     if hotel_scheme.name:
#         hotels_db[list_index_hotel]["name"] = hotel_scheme.name
#     if hotel_scheme.title:
#         hotels_db[list_index_hotel]["title"] = hotel_scheme.title
#     return {"status": "Ok"}
