from pydantic import BaseModel

from src.schemas.base import BasePatchSchema


class RoomsBaseSchema(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int


class RoomsWriteSchema(RoomsBaseSchema):
    pass


class RoomsPatchSchema(BasePatchSchema):
    hotel_id: int = None
    title: str = None
    description: str | None = None
    price: int = None
    quantity: int = None


class RoomsSchema(RoomsBaseSchema):
    id: int
