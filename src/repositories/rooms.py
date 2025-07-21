from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository, BaseM2MRepository
from src.repositories.mappers.mappers import RoomsDataMapper, RoomsRelsDataMapper
from src.repositories.utils.complex_queries import query_vacant_rooms
from src.support_tables.m2m import FacilitiesRoomsM2MTable


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomsDataMapper
    mapper_rels = RoomsRelsDataMapper

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # m2m repos
        self.rooms_facilities_m2m = RoomsFacilitiesM2MRepository(
            *args,
            main_column_name="room_id",
            target_column_name="facility_id",
            **kwargs,
        )

    async def get_vacant_rooms_by_hotel(
        self, date_from: date, date_to: date, hotel_id: int
    ):
        vacant_rooms_ids = query_vacant_rooms(
            date_from=date_from, date_to=date_to, hotel_id=hotel_id
        )
        # todo build general abstract select for relations in base repo
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsOrm.id.in_(vacant_rooms_ids))
        )
        # execute
        result = await self.session.execute(query)
        model_objects = result.scalars().all()
        return [self.mapper_rels.map_to_domain_entity(mo) for mo in model_objects]

    async def get_one_with_rels(self, **filter_by):
        # todo build general abstract select for relations in base repo
        # build query
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )
        # execute
        result = await self.session.execute(query)
        model_object = result.scalars().one()
        return self.mapper_rels.map_to_domain_entity(model_object)


class RoomsFacilitiesM2MRepository(BaseM2MRepository):
    table = FacilitiesRoomsM2MTable
