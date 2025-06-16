from datetime import date

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.utils.complex_queries import query_vacant_rooms
from src.schemas.rooms import RoomsSchema


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = RoomsSchema

    async def get_vacant_rooms_by_hotel(self, date_from: date, date_to: date, hotel_id: int):

        vacant_rooms_ids = query_vacant_rooms(date_from=date_from, date_to=date_to, hotel_id=hotel_id)

        return await self.get_many_filtered(RoomsOrm.id.in_(vacant_rooms_ids))
