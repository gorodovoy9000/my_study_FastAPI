from src.repositories.exceptions import NotFoundException, RoomQuantityZeroOnDateIntervalException
from src.schemas.bookings import BookingsSchema, BookingsRequestSchema, BookingsWriteSchema
from src.services.base import BaseService
from src.services.exceptions import RoomNotFoundException, NoVacantRoomsException
from src.services.utils import validate_date_to_is_bigger_than_date_from


class BookingsService(BaseService):
    async def get_bookings_all(self) -> list[BookingsSchema]:
        bookings = await self.db.bookings.get_all()
        return bookings

    async def get_bookings_my(self, user_id: int) -> list[BookingsSchema]:
        bookings = await self.db.bookings.get_many_filtered(user_id=user_id)
        return bookings

    async def add_booking(self, user_id: int, request_data: BookingsRequestSchema) -> BookingsSchema:
        validate_date_to_is_bigger_than_date_from(date_from=request_data.date_from, date_to=request_data.date_to)
        # get room
        try:
            room = await self.db.rooms.get_one(id=request_data.room_id)
        except NotFoundException as err:
            raise RoomNotFoundException from err
        # build booking create data
        create_data = BookingsWriteSchema(
            user_id=user_id, price=room.price, **request_data.model_dump()
        )
        # create booking
        try:
            data = await self.db.bookings.add_booking(create_data)
        except RoomQuantityZeroOnDateIntervalException as err:
            raise NoVacantRoomsException from err
        await self.db.commit()
        return data
