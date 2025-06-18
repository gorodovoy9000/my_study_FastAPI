from datetime import date

from src.models.facilities import facilities_rooms_at
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.utils.complex_queries import query_vacant_rooms
from src.repositories.utils.bulk_statements import add_bulk_to_table
from src.schemas.rooms import RoomsSchema, RoomsFacilitiesWrite


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = RoomsSchema

    async def get_vacant_rooms_by_hotel(self, date_from: date, date_to: date, hotel_id: int):

        vacant_rooms_ids = query_vacant_rooms(date_from=date_from, date_to=date_to, hotel_id=hotel_id)

        return await self.get_many_filtered(RoomsOrm.id.in_(vacant_rooms_ids))

    async def add_facilities_to_room(self, room_id: int, facilities_ids: list[int]):
        facilities_to_add = [RoomsFacilitiesWrite(room_id=room_id, facility_id=f_id) for f_id in facilities_ids]
        stmt = add_bulk_to_table(facilities_rooms_at, facilities_to_add)
        await self.session.execute(stmt)
