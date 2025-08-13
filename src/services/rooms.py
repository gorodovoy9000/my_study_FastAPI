from datetime import date

from sqlalchemy.exc import NoResultFound

from src.repositories.exceptions import (
    NotFoundException,
    ForeignKeyException,
)
from src.schemas.relations import RoomsRelsSchema
from src.schemas.rooms import (
    RoomsSchema,
    RoomsWriteSchema,
    RoomsPatchSchema,
    RoomsRequestPostSchema,
    RoomsRequestPatchSchema,
)
from src.services.base import BaseService
from src.services.exceptions import (
    HotelNotFoundException,
    RoomHasBookingsException,
    RoomNotFoundException,
    FacilitiesInvalidException,
)
from src.services.utils import validate_date_to_is_bigger_than_date_from


class RoomService(BaseService):
    async def get_rooms_filtered(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date,
    ) -> list[RoomsRelsSchema]:
        validate_date_to_is_bigger_than_date_from(date_from=date_from, date_to=date_to)
        rooms = await self.db.rooms.get_vacant_rooms_by_hotel(
            hotel_id=hotel_id,
            date_from=date_from,
            date_to=date_to,
        )
        return rooms

    async def get_room(self, room_id: int) -> RoomsRelsSchema:
        try:
            room = await self.db.rooms.get_one_with_rels(id=room_id)
        except NoResultFound:
            raise RoomNotFoundException
        return room

    async def add_room(self, request_data: RoomsRequestPostSchema) -> RoomsSchema:
        # create room
        create_data = RoomsWriteSchema(**request_data.model_dump())
        try:
            data = await self.db.rooms.add(create_data)
        except ForeignKeyException as err:
            raise HotelNotFoundException from err
        # add facilities to room by their ids
        if request_data.facilities_ids:
            await self._edit_room_facilities(room_id=data.id, facilities_ids=request_data.facilities_ids)
        await self.db.commit()
        return data

    async def edit_room(self, room_id: int, request_data: RoomsRequestPostSchema) -> None:
        # edit room
        update_data = RoomsWriteSchema(**request_data.model_dump())
        await self._edit_room(room_id=room_id, data=update_data)
        # change room facilities
        if request_data.facilities_ids is not None:
            await self._edit_room_facilities(room_id=room_id, facilities_ids=request_data.facilities_ids)
        await self.db.commit()

    async def edit_room_partially(self, room_id: int, request_data: RoomsRequestPatchSchema) -> None:
        # edit room partially
        update_data = RoomsPatchSchema(**request_data.model_dump(exclude_unset=True))
        await self._edit_room(room_id=room_id, data=update_data, partial_update=True)
        # change room facilities
        if request_data.facilities_ids is not None:
            await self._edit_room_facilities(room_id=room_id, facilities_ids=request_data.facilities_ids)
        await self.db.commit()

    async def delete_room(self, room_id: int) -> None:
        try:
            await self.db.rooms.delete(id=room_id)
        except NotFoundException as err:
            raise RoomNotFoundException from err
        except ForeignKeyException as err:
            raise RoomHasBookingsException from err
        await self.db.commit()

    async def _edit_room(self, room_id: int, data: RoomsPatchSchema | RoomsWriteSchema, partial_update=False) -> None:
        try:
            await self.db.rooms.edit(data, id=room_id, partial_update=partial_update)
        except NotFoundException as err:
            raise RoomNotFoundException from err
        except ForeignKeyException as err:
            raise HotelNotFoundException from err

    async def _edit_room_facilities(self, room_id: int, facilities_ids: list[int]) -> None:
        try:
            await self.db.rooms.rooms_facilities_m2m.edit(room_id, facilities_ids)
        except ForeignKeyException as err:
            raise FacilitiesInvalidException from err
