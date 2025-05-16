from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

from schemas import HotelScheme, HotelWriteScheme, HotelPatchScheme

router = APIRouter(prefix="/hotels", tags=["hotels"])

################# fake db
# fake db
hotels_db = [
    {"id": 1, "title": "Сочи", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Москва", "name": "moscow"},
    {"id": 4, "title": "Санкт-Петербург", "name": "spb"},
    {"id": 5, "title": "Тула", "name": "tula"},
    {"id": 6, "title": "Нью-Йорк", "name": "ny"},
    {"id": 7, "title": "Берлин", "name": "berlin"},
    {"id": 8, "title": "Владимир", "name": "vladimir"},
]
# increment imitation
max_id = len(hotels_db)
#############################


@router.get("")
async def get_hotels(
        page: Annotated[
            int, Query(
                title="Page",
                description="Pagination page number",
            )
        ] = 1,
        per_page: Annotated[
            int, Query(
                title="Per Page",
                description="Pagination items per page",
            )
        ] = 3,
) -> list[HotelScheme]:
    total = len(hotels_db)
    start = (page - 1) * per_page
    end = page * per_page
    return [HotelScheme.model_validate(ho, from_attributes=True) for ho in hotels_db[start:end]]


@router.delete("/{hotel_id}", status_code=204)
async def delete_hotel(hotel_id: int):
    # get hotel
    list_index_hotel = None
    for i, hotel in enumerate (hotels_db):
        if hotel["id"] == hotel_id:
            list_index_hotel = i
    # not found by id
    if list_index_hotel is None:
        raise HTTPException(status_code=404, detail="Hotel not found")
    # delete from list
    hotels_db.pop(list_index_hotel)
    return {"status": "Ok"}


@router.post("", status_code=201)
async def create_hotel(hotel_scheme: HotelWriteScheme) -> HotelScheme:
    # check if hotel already created
    for hotel in hotels_db:
        if hotel["name"] == hotel_scheme.name:
            raise HTTPException(status_code=422, detail="Hotel already exists")
    # create hotel
    global max_id
    max_id += 1
    created_hotel_data = {"id": max_id, "name": hotel_scheme.name, "title": hotel_scheme.title}
    hotels_db.append(created_hotel_data)
    return HotelScheme.model_validate(created_hotel_data, from_attributes=True)


@router.put("/{hotel_id}", status_code=204)
async def update_hotel(
        hotel_id: int,
        hotel_scheme: HotelPatchScheme,
):
    # get hotel
    list_index_hotel = None
    for i, hotel in enumerate(hotels_db):
        if hotel["id"] == hotel_id:
            list_index_hotel = i
    # not found by id
    if list_index_hotel is None:
        raise HTTPException(status_code=404, detail="Hotel not found")
    # replace hotel data
    hotels_db[list_index_hotel] = {"id": hotel_id, "name": hotel_scheme.name, "title": hotel_scheme.title}
    return {"status": "Ok"}


@router.patch("/{hotel_id}", status_code=204)
async def update_hotel(
        hotel_id: int,
        hotel_scheme: HotelPatchScheme,
):
    # get hotel
    list_index_hotel = None
    for i, hotel in enumerate(hotels_db):
        if hotel["id"] == hotel_id:
            list_index_hotel = i
    # not found by id
    if list_index_hotel is None:
        raise HTTPException(status_code=404, detail="Hotel not found")
    # partial update
    if hotel_scheme.name:
        hotels_db[list_index_hotel]["name"] = hotel_scheme.name
    if hotel_scheme.title:
        hotels_db[list_index_hotel]["title"] = hotel_scheme.title
    return {"status": "Ok"}
