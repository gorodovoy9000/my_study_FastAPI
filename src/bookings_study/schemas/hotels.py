from typing import Annotated

from pydantic import AfterValidator, BaseModel

from bookings_study.schemas.base import BasePatchSchema, BaseResponseSchema
from bookings_study.schemas.utils.validators import is_string_not_empty


class HotelsBaseSchema(BaseModel):
    title: Annotated[str, AfterValidator(is_string_not_empty)]
    location: Annotated[str, AfterValidator(is_string_not_empty)]


class HotelsWriteSchema(HotelsBaseSchema):
    pass


class HotelsPatchSchema(BasePatchSchema):
    title: Annotated[str, AfterValidator(is_string_not_empty)] = None
    location: Annotated[str, AfterValidator(is_string_not_empty)] = None


class HotelsSchema(HotelsBaseSchema):
    id: int


class HotelsResponseSchema(BaseResponseSchema):
    data: list[HotelsSchema]
