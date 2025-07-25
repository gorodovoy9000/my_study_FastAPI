from src.repositories.exceptions import NotFoundException
from src.schemas.facilities import FacilitiesSchema, FacilitiesWriteSchema, FacilitiesPatchSchema
from src.services.base import BaseService
from src.services.exceptions import FacilityNotFoundException


class FacilityService(BaseService):
    async def get_facilities_all(self, limit, offset) -> list[FacilitiesSchema]:
        data = await self.db.facilities.get_many_filtered(limit=limit, offset=offset)
        return data

    async def get_facility(self, facility_id: int) -> FacilitiesSchema:
        try:
            data = await self.db.facilities.get_one(id=facility_id)
        except NotFoundException as err:
            raise FacilityNotFoundException from err
        return data

    async def add_facility(self, data_create: FacilitiesWriteSchema) -> FacilitiesSchema:
        data = await self.db.facilities.add(data_create)
        await self.db.commit()
        return data

    async def edit_facility(self, facility_id: int, data_update: FacilitiesWriteSchema) -> None:
        try:
            await self.db.facilities.edit(data_update, id=facility_id)
        except NotFoundException as err:
            raise FacilityNotFoundException from err
        await self.db.commit()

    async def edit_facility_partially(self, facility_id: int, data_update: FacilitiesPatchSchema) -> None:
        try:
            await self.db.facilities.edit(data_update, id=facility_id, partial_update=True)
        except NotFoundException as err:
            raise FacilityNotFoundException from err
        await self.db.commit()

    async def delete_facility(self, facility_id: int) -> None:
        try:
            await self.db.facilities.delete(id=facility_id)
        except NotFoundException as err:
            raise FacilityNotFoundException from err
        await self.db.commit()
