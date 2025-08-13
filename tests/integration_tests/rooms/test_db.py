from src.schemas.rooms import RoomsWriteSchema


async def test_room_crud(db):
    # create room
    create_data = RoomsWriteSchema(
        hotel_id=1,
        title="Sub-standard",
        description="For poor losers",
        price=150,
        quantity=10,
    )
    created_room = await db.rooms.add(create_data)

    # get created room
    room = await db.rooms.get_one(id=created_room.id)
    assert room.model_dump(exclude={"id"}) == create_data.model_dump()

    # update room
    update_data = RoomsWriteSchema(
        hotel_id=1,
        title="Cell for 1 person",
        description="Like cell in prison",
        price=100,
        quantity=10,
    )
    await db.rooms.edit(update_data, id=created_room.id)
    room = await db.rooms.get_one(id=created_room.id)
    assert room.model_dump(exclude={"id"}) == update_data.model_dump()

    # delete room
    await db.rooms.delete(id=created_room.id)
    room = await db.rooms.get_one_or_none(id=created_room.id)
    assert not room
