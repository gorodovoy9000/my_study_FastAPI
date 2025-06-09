from pydantic import BaseModel

from src.schemas.base import BasePatchSchema


class HotelsBaseSchema(BaseModel):
    title: str
    location: str


class HotelsWriteSchema(HotelsBaseSchema):
    pass


class HotelsPatchSchema(BasePatchSchema):
    title: str = None
    location: str = None


class HotelsSchema(HotelsBaseSchema):
    id: int
