from datetime import date

from src.schemas.bookings import BookingsWriteSchema


async def test_add_booking(db):
    user_id = (await db.users.get_many_filtered(limit=1))[0].id
    room_id = (await db.rooms.get_many_filtered(limit=1))[0].id
    booking_data = BookingsWriteSchema(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2025, month=8, day=10),
        date_to=date(year=2025, month=8, day=20),
        price=100,
    )
    await db.bookings.add(booking_data)
    await db.commit()
