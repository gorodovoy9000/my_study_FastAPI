from typing import Annotated

from pydantic import BaseModel, Field

from bookings_study.schemas.base import BasePatchSchema, BaseResponseSchema


class FacilitiesBaseSchema(BaseModel):
    title: Annotated[str, Field(min_length=1)]


class FacilitiesWriteSchema(FacilitiesBaseSchema):
    pass


class FacilitiesPatchSchema(BasePatchSchema):
    title: Annotated[str, Field(min_length=1)] = None


class FacilitiesSchema(FacilitiesBaseSchema):
    id: int

class FacilitiesResponseSchema(BaseResponseSchema):
    data: list[FacilitiesSchema]
