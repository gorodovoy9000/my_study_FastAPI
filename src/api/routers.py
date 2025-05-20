from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import insert, select, delete

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
        query = select(HotelsOrm)
        # optional substring filter by title, location
        if title:
            query = query.where(HotelsOrm.title.icontains(title.strip().lower()))
        if location:
            query = query.where(HotelsOrm.location.icontains(location.strip().lower()))
        # pagination
        query = (
            query
            .limit(pagination.per_page)
            .offset(pagination.per_page * (pagination.page - 1))
        )
        result = await session.execute(query)
        items_orm = result.scalars().all()
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
async def create_hotel(hotel_scheme: HotelWriteScheme):
    async with async_session_maker() as session:
        stms = (
            insert(HotelsOrm)
            .values(**hotel_scheme.model_dump())
            .returning(HotelsOrm.id)
        )
        # debug stmt print
        print(stms.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await session.execute(stms)
        created_item_id = result.scalars().first()
        await session.commit()
    return {"id": created_item_id}


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
