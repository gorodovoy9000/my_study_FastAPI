from pydantic import BaseModel

from src.schemas.base import BasePatchSchema


class HotelBaseSchema(BaseModel):
    title: str
    location: str


class HotelWriteSchema(HotelBaseSchema):
    pass


class HotelPatchSchema(BasePatchSchema):
    title: str = None
    location: str = None


class HotelSchema(HotelBaseSchema):
    id: int
