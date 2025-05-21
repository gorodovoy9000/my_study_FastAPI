from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy.exc import MultipleResultsFound, NoResultFound

from repositories.hotels import HotelsRepository
from src.api.dependencies import PaginationDep
from src.database import async_session_maker
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


@router.post("", status_code=201)
async def create_hotel(scheme_create: HotelWriteScheme):
    async with async_session_maker() as session:
        item_orm = await HotelsRepository(session).add(scheme_create)
        # transaction commit MUST stay here!
        await session.commit()
    return {"status": "Ok", "data": item_orm}


@router.delete("/{hotel_id}", status_code=204)
async def delete_hotel(hotel_id: int):
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
async def update_hotel(hotel_id: int, scheme_update: HotelWriteScheme):
    async with async_session_maker() as session:
        try:
            await HotelsRepository(session).edit(scheme_update, id=hotel_id)
            await session.commit()
        except MultipleResultsFound:
            raise HTTPException(status_code=422, detail="Multiple hotels found, only one allowed")
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Hotel not found")
    return {"status": "Ok"}


@router.patch("/{hotel_id}", status_code=204)
async def partial_update_hotel(hotel_id: int, scheme_patch: HotelPatchScheme):
    async with async_session_maker() as session:
        try:
            await HotelsRepository(session).edit(scheme_patch, partial_update=True, id=hotel_id)
            await session.commit()
        except MultipleResultsFound:
            raise HTTPException(status_code=422, detail="Multiple hotels found, only one allowed")
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Hotel not found")
    return {"status": "Ok"}
