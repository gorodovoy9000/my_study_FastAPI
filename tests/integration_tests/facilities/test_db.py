from src.schemas.facilities import FacilitiesWriteSchema


async def test_facility_crud(db):
    # create facility
    create_data = FacilitiesWriteSchema(title="shower")
    created_facility = await db.facilities.add(create_data)

    # get created facility
    facility = await db.facilities.get_one(id=created_facility.id)
    assert facility.model_dump(exclude={"id"}) == create_data.model_dump()

    # update facility
    update_data = FacilitiesWriteSchema(title="bath")
    await db.facilities.edit(update_data, id=created_facility.id)
    facility = await db.facilities.get_one(id=created_facility.id)
    assert facility.model_dump(exclude={"id"}) == update_data.model_dump()

    # delete facility
    await db.facilities.delete(id=created_facility.id)
    facility = await db.facilities.get_one_or_none(id=created_facility.id)
    assert not facility
