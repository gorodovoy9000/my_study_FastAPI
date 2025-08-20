from datetime import date

from sqlalchemy import select

from bookings_study.models.hotels import HotelsOrm
from bookings_study.models.rooms import RoomsOrm
from bookings_study.repositories.base import BaseRepository
from bookings_study.repositories.mappers.mappers import HotelDataMapper
from bookings_study.repositories.utils.complex_queries import query_vacant_rooms


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    mapper = HotelDataMapper

    # async def get_all(self, location: str, title: str, limit: int, offset: int) -> list[HotelsSchema]:
    #     query = select(HotelsOrm)
    #     # optional substring filter by title, location
    #     if title:
    #         query = query.where(HotelsOrm.title.icontains(title.strip().lower()))
    #     if location:
    #         query = query.where(HotelsOrm.location.icontains(location.strip().lower()))
    #     # pagination
    #     query = query.limit(limit).offset(offset)
    #     result = await self.session.execute(query)
    #     model_objects = result.scalars().all()
    #     return [HotelsSchema.model_validate(mo, from_attributes=True) for mo in model_objects]

    async def get_hotels_with_vacant_rooms(
        self,
        date_from: date,
        date_to: date,
        location: str | None,
        title: str | None,
        limit: int,
        offset: int,
    ):
        vacant_rooms_ids = query_vacant_rooms(date_from=date_from, date_to=date_to)

        hotels_ids_by_vacant_rooms = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(vacant_rooms_ids))
        )

        # filtering
        filters = [
            HotelsOrm.id.in_(hotels_ids_by_vacant_rooms),
        ]
        if title:
            filters.append(HotelsOrm.title.icontains(title.strip().lower()))
        if location:
            filters.append(HotelsOrm.location.icontains(location.strip().lower()))

        # execute and get data
        data = await self.get_many_filtered(
            *filters,
            limit=limit,
            offset=offset,
        )
        return data
