from datetime import date

from bookings_study.schemas.bookings import BookingsWriteSchema


async def test_booking_crud(db):
    # get any user and room
    user_id = (await db.users.get_many_filtered(limit=1))[0].id
    room_id = (await db.rooms.get_many_filtered(limit=1))[0].id

    # create booking
    create_data = BookingsWriteSchema(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2025, month=8, day=10),
        date_to=date(year=2025, month=8, day=20),
        price=100,
    )
    created_booking = await db.bookings.add(create_data)

    # get created booking
    booking = await db.bookings.get_one(id=created_booking.id)
    assert booking.model_dump(exclude={"id"}) == create_data.model_dump()

    # update booking
    update_data = BookingsWriteSchema(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2025, month=9, day=10),
        date_to=date(year=2025, month=9, day=20),
        price=200,
    )
    await db.bookings.edit(update_data, id=created_booking.id)
    booking = await db.bookings.get_one(id=created_booking.id)
    assert booking.model_dump(exclude={"id"}) == update_data.model_dump()

    # delete booking
    await db.bookings.delete(id=created_booking.id)
    booking = await db.bookings.get_one_or_none(id=created_booking.id)
    assert not booking
