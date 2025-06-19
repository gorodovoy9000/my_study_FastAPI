from pydantic import BaseModel, Field

from src.schemas.base import BasePatchSchema


class RoomsBaseSchema(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int


class RoomsRequestPostSchema(RoomsBaseSchema):
    facilities_ids: list[int] = None


class RoomsWriteSchema(RoomsBaseSchema):
    pass


class RoomsRequestPatchSchema(BasePatchSchema):
    hotel_id: int = None
    title: str = None
    description: str | None = None
    price: int = None
    quantity: int = None
    facilities_ids: list[int] = Field(None, exclude=True)


class RoomsPatchSchema(BasePatchSchema):
    hotel_id: int = None
    title: str = None
    description: str | None = None
    price: int = None
    quantity: int = None


class RoomsSchema(RoomsBaseSchema):
    id: int
