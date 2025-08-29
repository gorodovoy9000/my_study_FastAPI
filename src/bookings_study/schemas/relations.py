from bookings_study.schemas.base import BaseResponseSchema
from bookings_study.schemas.facilities import FacilitiesSchema
from bookings_study.schemas.rooms import RoomsSchema


class RoomsRelsSchema(RoomsSchema):
    facilities: list[FacilitiesSchema]


class RoomsResponseRelsSchema(BaseResponseSchema):
    data: list[RoomsRelsSchema]
