from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Path
from sqlalchemy.exc import MultipleResultsFound, NoResultFound

from src.api.dependencies import IdDep, PaginationDep
from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository
from src.schemas import HotelSchema, HotelWriteSchema, HotelPatchSchema

router = APIRouter(prefix="/hotels", tags=["hotels"])


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        title: Annotated[str | None, Query(description="Filter by substring hotel title")] = None,
        location: Annotated[str | None, Query(description="Filter by substring hotel location")] = None,
) -> list[HotelSchema]:
    async with async_session_maker() as session:
        data = await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=pagination.per_page,
            offset=pagination.per_page * (pagination.page - 1),
        )
    return data


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: IdDep) -> HotelSchema:
    async with async_session_maker() as session:
        try:
            data = await HotelsRepository(session).get_one(id=hotel_id)
        except MultipleResultsFound:
            raise HTTPException(status_code=422, detail="Multiple hotels found, only one allowed")
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Hotel not found")
    return data


@router.post("", status_code=201)
async def create_hotel(schema_create: HotelWriteSchema):
    async with async_session_maker() as session:
        data = await HotelsRepository(session).add(schema_create)
        # transaction commit MUST stay here!
        await session.commit()
    return {"status": "Ok", "data": data}


@router.delete("/{hotel_id}", status_code=204)
async def delete_hotel(hotel_id: IdDep):
    async with async_session_maker() as session:
        try:
            await HotelsRepository(session).delete(id=hotel_id)
            await session.commit()
        except MultipleResultsFound:
            raise HTTPException(status_code=422, detail="Multiple hotels found, only one allowed")
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Hotel not found")
    return {"status": "Ok"}


@router.put("/{hotel_id}", status_code=204)
async def update_hotel(hotel_id: IdDep, schema_update: HotelWriteSchema):
    async with async_session_maker() as session:
        try:
            await HotelsRepository(session).edit(schema_update, id=hotel_id)
            await session.commit()
        except MultipleResultsFound:
            raise HTTPException(status_code=422, detail="Multiple hotels found, only one allowed")
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Hotel not found")
    return {"status": "Ok"}


@router.patch("/{hotel_id}", status_code=204)
async def partial_update_hotel(hotel_id: IdDep, schema_patch: HotelPatchSchema):
    async with async_session_maker() as session:
        try:
            await HotelsRepository(session).edit(schema_patch, partial_update=True, id=hotel_id)
            await session.commit()
        except MultipleResultsFound:
            raise HTTPException(status_code=422, detail="Multiple hotels found, only one allowed")
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Hotel not found")
    return {"status": "Ok"}
