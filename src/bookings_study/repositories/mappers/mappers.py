from bookings_study.models.bookings import BookingsOrm
from bookings_study.models.facilities import FacilitiesOrm
from bookings_study.models.hotels import HotelsOrm
from bookings_study.models.rooms import RoomsOrm
from bookings_study.models.users import UsersOrm
from bookings_study.repositories.mappers.base import BaseDataMapper
from bookings_study.schemas.bookings import BookingsSchema
from bookings_study.schemas.facilities import FacilitiesSchema
from bookings_study.schemas.hotels import HotelsSchema
from bookings_study.schemas.relations import RoomsRelsSchema
from bookings_study.schemas.rooms import RoomsSchema
from bookings_study.schemas.users import UsersSchema


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
