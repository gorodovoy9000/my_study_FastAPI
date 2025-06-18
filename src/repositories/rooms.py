from datetime import date

from sqlalchemy import select

from src.models.facilities import facilities_rooms_at
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.utils.complex_queries import query_vacant_rooms
from src.repositories.utils.bulk_statements import add_bulk_to_table, delete_bulk_to_table
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

    async def change_facilities_of_room(self, room_id, given_facilities_ids: list[int]):
        # todo - refactor for more general and more convenient m2m!!
        # select m2m objects of given room
        query_m2m = select(facilities_rooms_at.c.facility_id).filter_by(room_id=room_id)
        result = await self.session.execute(query_m2m)
        db_m2m = set(result.scalars().all())
        given_m2m = set(given_facilities_ids)
        # compare given and db facilities ids - form to add and to delete
        to_delete_m2m = db_m2m - given_m2m
        to_add_m2m = given_m2m - db_m2m
        # delete m2m objects
        if to_delete_m2m:
            filters = [
                facilities_rooms_at.c.room_id == room_id,
                facilities_rooms_at.c.facility_id.in_(to_delete_m2m),
            ]
            delete_stmt = delete_bulk_to_table(facilities_rooms_at, *filters)
            await self.session.execute(delete_stmt)
        # add m2m objects
        if to_add_m2m:
            facilities_to_add = [RoomsFacilitiesWrite(room_id=room_id, facility_id=f_id) for f_id in to_add_m2m]
            add_stmt = add_bulk_to_table(facilities_rooms_at, facilities_to_add)
            await self.session.execute(add_stmt)
