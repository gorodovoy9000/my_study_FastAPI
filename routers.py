from fastapi import APIRouter, Body, HTTPException


router = APIRouter(prefix="/hotels", tags=["hotels"])

################# fake db
# fake db
hotels_db = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
]
# increment imitation
max_id = len(hotels_db)
#############################


@router.get("")
async def get_hotels():
    return hotels_db


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


@router.post("", status_code=201)
async def create_hotel(
        hotel_name: str = Body(),
        hotel_title: str = Body(),
):
    # check if hotel already created
    for hotel in hotels_db:
        if hotel["name"] == hotel_name:
            raise HTTPException(status_code=422, detail="Hotel already exists")
    # create hotel
    created_hotel_data = {"id": max_id+1, "title": hotel_title, "name": hotel_name}
    hotels_db.append(created_hotel_data)
    return created_hotel_data


@router.put("/{hotel_id}", status_code=204)
async def update_hotel(
        hotel_id: int,
        hotel_name: str = Body(),
        hotel_title: str = Body(),
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
    hotels_db[list_index_hotel] = {"id": hotel_id, "name": hotel_name, "title": hotel_title}


@router.patch("/{hotel_id}", status_code=204)
async def update_hotel(
        hotel_id: int,
        hotel_name: str | None = Body(default=None),
        hotel_title: str| None = Body(default=None),
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
    if hotel_name:
        hotels_db[list_index_hotel]["name"] = hotel_name
    if hotel_title:
        hotels_db[list_index_hotel]["title"] = hotel_title