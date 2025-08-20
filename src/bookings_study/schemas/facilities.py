from pydantic import BaseModel

from bookings_study.schemas.base import BasePatchSchema


class FacilitiesBaseSchema(BaseModel):
    title: str


class FacilitiesWriteSchema(FacilitiesBaseSchema):
    pass


class FacilitiesPatchSchema(BasePatchSchema):
    title: str = None


class FacilitiesSchema(FacilitiesBaseSchema):
    id: int
