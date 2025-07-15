from datetime import date

from sqlalchemy import func, select

from src.exceptions import NoVacantRoomsException
from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm
from src.schemas.bookings import BookingsWriteSchema
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingsDataMapper


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingsDataMapper

    async def get_bookings_with_today_checkin(self):
        query = (
            select(BookingsOrm)
            .filter(BookingsOrm.date_from == date.today())
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(bo) for bo in result.scalars().all()]

    async def add_booking(self, create_booking_data: BookingsWriteSchema):
        # get bookings of room
        query_room_bookings = (
            select(func.count("*").label("room_bookings"))
            .select_from(BookingsOrm)
            .filter(
                BookingsOrm.date_from <= create_booking_data.date_to,
                BookingsOrm.date_to >= create_booking_data.date_from,
                BookingsOrm.room_id == create_booking_data.room_id,
            )
        )
        result = await self.session.execute(query_room_bookings)
        room_bookings = result.scalars().one()
        # get room vacant quantity
        query_vacant_room_quantity = (
            select(
                (RoomsOrm.quantity - room_bookings).label("vacant_rooms")
            )
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id == create_booking_data.room_id)
        )
        result = await self.session.execute(query_vacant_room_quantity)
        room_vacant_quantity = result.scalars().one()
        # print(room_vacant_quantity)
        # validate there are some vacate rooms
        if room_vacant_quantity > 0:
            return await self.add(create_booking_data)
        msg = "No vacant rooms remains"
        raise NoVacantRoomsException(msg)
