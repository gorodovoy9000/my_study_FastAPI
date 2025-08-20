from datetime import date

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload

from bookings_study.repositories.exceptions import NotFoundException
from bookings_study.models.rooms import RoomsOrm
from bookings_study.repositories.base import BaseRepository, BaseM2MRepository
from bookings_study.repositories.mappers.mappers import (
    RoomsDataMapper,
    RoomsRelsDataMapper,
)
from bookings_study.repositories.utils.complex_queries import query_vacant_rooms
from bookings_study.support_tables.m2m import FacilitiesRoomsM2MTable


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
            select(RoomsOrm)
            .options(selectinload(RoomsOrm.facilities))
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
            select(RoomsOrm)
            .options(selectinload(RoomsOrm.facilities))
            .filter_by(**filter_by)
        )
        # execute
        result = await self.session.execute(query)
        try:
            model_object = result.scalar_one()
        except NoResultFound as err:
            raise NotFoundException from err
        return self.mapper_rels.map_to_domain_entity(model_object)


class RoomsFacilitiesM2MRepository(BaseM2MRepository):
    table = FacilitiesRoomsM2MTable
