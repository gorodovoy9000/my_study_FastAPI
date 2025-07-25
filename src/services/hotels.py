from datetime import date

from src.exceptions import validate_date_to_is_bigger_than_date_from
from src.schemas.hotels import HotelsWriteSchema, HotelsPatchSchema, HotelsSchema
from src.services.base import BaseService


class HotelService(BaseService):
    async def get_hotels_filtered(
            self,
            date_from: date,
            date_to: date,
            location: str | None,
            title: str | None,
            limit: int,
            offset: int,
    ) -> list[HotelsSchema]:
        validate_date_to_is_bigger_than_date_from(date_from=date_from, date_to=date_to)
        hotels =  await self.db.hotels.get_hotels_with_vacant_rooms(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=limit,
            offset=offset,
        )
        return hotels

    async def get_hotel(self, hotel_id: int) -> HotelsSchema:
        hotel = await self.db.hotels.get_one(id=hotel_id)
        return hotel

    async def add_hotel(self, data: HotelsWriteSchema) -> HotelsSchema:
        hotel = await self.db.hotels.add(data)
        await self.db.commit()
        return hotel

    async def edit_hotel(self, hotel_id: int, data: HotelsWriteSchema) -> None:
        await self.db.hotels.edit(data, id=hotel_id)
        await self.db.commit()

    async def edit_hotel_partially(self, hotel_id: int, data: HotelsPatchSchema) -> None:
        await self.db.hotels.edit(data, partial_update=True, id=hotel_id)
        await self.db.commit()

    async def delete_hotel(self, hotel_id: int) -> None:
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()
