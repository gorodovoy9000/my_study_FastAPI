from datetime import date

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository, BaseM2MRepository
from src.repositories.utils.complex_queries import query_vacant_rooms
from src.support_tables.m2m import FacilitiesRoomsM2MTable
from src.schemas.rooms import RoomsSchema


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = RoomsSchema

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # m2m repos
        self.rooms_facilities_m2m = RoomsFacilitiesM2MRepository(
            *args,
            main_column_name="room_id",
            target_column_name="facility_id",
            **kwargs
        )

    async def get_vacant_rooms_by_hotel(self, date_from: date, date_to: date, hotel_id: int):

        vacant_rooms_ids = query_vacant_rooms(date_from=date_from, date_to=date_to, hotel_id=hotel_id)

        return await self.get_many_filtered(RoomsOrm.id.in_(vacant_rooms_ids))


class RoomsFacilitiesM2MRepository(BaseM2MRepository):
    table = FacilitiesRoomsM2MTable
