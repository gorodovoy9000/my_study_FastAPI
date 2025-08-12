from src.schemas.hotels import HotelsWriteSchema


async def test_hotel_crud(db):
    # create hotel
    create_data = HotelsWriteSchema(title="Hotel 5 stars", location="Sochi")
    created_hotel = await db.hotels.add(create_data)

    # get created hotel
    hotel = await db.hotels.get_one(id=created_hotel.id)
    assert hotel.model_dump(exclude={"id"}) == create_data.model_dump()

    # update hotel
    update_data = HotelsWriteSchema(title="Hotel 3 stars", location="Dushanbe")
    await db.hotels.edit(update_data, id=created_hotel.id)
    hotel = await db.hotels.get_one(id=created_hotel.id)
    assert hotel.model_dump(exclude={"id"}) == update_data.model_dump()

    # delete hotel
    await db.hotels.delete(id=created_hotel.id)
    hotel = await db.hotels.get_one_or_none(id=created_hotel.id)
    assert not hotel
