from typing import Annotated

from pydantic import BaseModel, Field

from bookings_study.schemas.base import BasePatchSchema, BaseResponseSchema

class HotelsBaseSchema(BaseModel):
    title: Annotated[str, Field(min_length=1)]
    location: Annotated[str, Field(min_length=1)]


class HotelsWriteSchema(HotelsBaseSchema):
    pass


class HotelsPatchSchema(BasePatchSchema):
    title: Annotated[str, Field(min_length=1)] = None
    location: Annotated[str, Field(min_length=1)] = None


class HotelsSchema(HotelsBaseSchema):
    id: int


class HotelsResponseSchema(BaseResponseSchema):
    data: list[HotelsSchema]
