from sqlalchemy import select

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.schemas.rooms import RoomsSchema

class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = RoomsSchema

    async def get_rooms_by_hotel(self, hotel_id: int) -> list[schema]:
        query = select(self.model).filter_by(hotel_id=hotel_id)
        result = await self.session.execute(query)
        model_objects = result.scalars().all()
        return [self.schema.model_validate(mo, from_attributes=True) for mo in model_objects]
