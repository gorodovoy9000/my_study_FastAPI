from datetime import date

from sqlalchemy import func, select

from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.schemas.rooms import RoomsSchema


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = RoomsSchema

    async def get_filtered_by_date(self, hotel_id: int, date_from: date, date_to: date):
        cte_rooms_count_result = (
            select(BookingsOrm.room_id, func.count("*").label("rooms_booked"))
            .select_from(BookingsOrm)
            .filter(
                BookingsOrm.date_from <= date_to,
                BookingsOrm.date_to >= date_from,
            )
            .group_by(BookingsOrm.room_id)
            .cte(name="rooms_count_result")
        )

        cte_rooms_remaining_result = (
            select(
                RoomsOrm.id.label("room_id"),
                (RoomsOrm.quantity - func.coalesce(cte_rooms_count_result.c.rooms_booked, 0)).label("rooms_remaining")
            )
            .select_from(RoomsOrm)
            .outerjoin(cte_rooms_count_result, RoomsOrm.id == cte_rooms_count_result.c.room_id)
            .cte("rooms_remaining_result")
        )

        query_rooms_ids_by_hotel = (
            select(RoomsOrm.id)
            .select_from(RoomsOrm)
            .filter_by(hotel_id=hotel_id)
            .subquery(name="rooms_ids_of_hotel")
        )

        vacant_rooms_ids = (
            select(cte_rooms_remaining_result.c.room_id)
            .select_from(cte_rooms_remaining_result)
            .filter(
                cte_rooms_remaining_result.c.rooms_remaining > 0,
                cte_rooms_remaining_result.c.room_id.in_(query_rooms_ids_by_hotel)
            )
        )

        # print(vacant_rooms_ids.compile(compile_kwargs={'literal_binds': True}))

        return await self.get_many_filtered(RoomsOrm.id.in_(vacant_rooms_ids))
