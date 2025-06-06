from sqlalchemy import select

from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository
from src.schemas.hotels import HotelSchema


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = HotelSchema

    async def get_all(self, location: str, title: str, limit: int, offset: int) -> list[HotelSchema]:
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
        return [HotelSchema.model_validate(mo, from_attributes=True) for mo in model_objects]
