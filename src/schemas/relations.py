from src.schemas.facilities import FacilitiesSchema
from src.schemas.rooms import RoomsSchema


class RoomsRelsSchema(RoomsSchema):
    facilities: list[FacilitiesSchema]
