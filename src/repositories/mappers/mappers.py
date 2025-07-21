from src.models.bookings import BookingsOrm
from src.models.facilities import FacilitiesOrm
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.models.users import UsersOrm
from src.repositories.mappers.base import BaseDataMapper
from src.schemas.bookings import BookingsSchema
from src.schemas.facilities import FacilitiesSchema
from src.schemas.hotels import HotelsSchema
from src.schemas.relations import RoomsRelsSchema
from src.schemas.rooms import RoomsSchema
from src.schemas.users import UsersSchema


class HotelDataMapper(BaseDataMapper):
    ModelOrmCls = HotelsOrm
    SchemaCls = HotelsSchema


class RoomsDataMapper(BaseDataMapper):
    ModelOrmCls = RoomsOrm
    SchemaCls = RoomsSchema


class RoomsRelsDataMapper(BaseDataMapper):
    ModelOrmCls = RoomsOrm
    SchemaCls = RoomsRelsSchema


class BookingsDataMapper(BaseDataMapper):
    ModelOrmCls = BookingsOrm
    SchemaCls = BookingsSchema


class FacilitiesDataMapper(BaseDataMapper):
    ModelOrmCls = FacilitiesOrm
    SchemaCls = FacilitiesSchema


class UsersDataMapper(BaseDataMapper):
    ModelOrmCls = UsersOrm
    SchemaCls = UsersSchema
