from datetime import date

from sqlalchemy import select

from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.utils.complex_queries import query_vacant_rooms
from src.schemas.hotels import HotelsSchema


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = HotelsSchema

    async def get_all(self, location: str, title: str, limit: int, offset: int) -> list[HotelsSchema]:
        query = select(HotelsOrm)
        # optional substring filter by title, location
        if title:
            query = query.where(HotelsOrm.title.icontains(title.strip().lower()))
        if location:
            query = query.where(HotelsOrm.location.icontains(location.strip().lower()))
        # pagination
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        model_objects = result.scalars().all()
        return [HotelsSchema.model_validate(mo, from_attributes=True) for mo in model_objects]

    async def get_vacant_rooms(self, date_from: date, date_to: date):
        vacant_rooms_ids = query_vacant_rooms(date_from=date_from, date_to=date_to)

        hotels_ids_by_vacant_rooms = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(vacant_rooms_ids))
        )
        return await self.get_many_filtered(HotelsOrm.id.in_(hotels_ids_by_vacant_rooms))
