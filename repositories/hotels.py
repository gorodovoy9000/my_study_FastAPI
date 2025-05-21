from sqlalchemy import select

from src.models import HotelsOrm
from repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(self, location, title, limit, offset):
        query = select(HotelsOrm)
        # optional substring filter by title, location
        if title:
            query = query.where(HotelsOrm.title.icontains(title.strip().lower()))
        if location:
            query = query.where(HotelsOrm.location.icontains(location.strip().lower()))
        # pagination
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return result.scalars().all()
