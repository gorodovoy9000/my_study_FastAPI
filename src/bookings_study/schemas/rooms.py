from typing import Annotated

from pydantic import BaseModel, Field

from bookings_study.schemas.base import BasePatchSchema, BaseResponseSchema


class RoomsBaseSchema(BaseModel):
    hotel_id: Annotated[int, Field(gt=0)]
    title: Annotated[str, Field(min_length=1)]
    description: str | None = None
    price: Annotated[int, Field(gt=0)]
    quantity: Annotated[int, Field(gt=0)]


class RoomsRequestPostSchema(RoomsBaseSchema):
    facilities_ids: list[Annotated[int, Field(gt=0)]] = None


class RoomsWriteSchema(RoomsBaseSchema):
    pass


class RoomsRequestPatchSchema(BasePatchSchema):
    hotel_id: Annotated[int, Field(gt=0)] = None
    title: Annotated[str, Field(min_length=1)] = None
    description: str | None = None
    price: Annotated[int, Field(gt=0)] = None
    quantity: Annotated[int, Field(gt=0)] = None
    facilities_ids: list[Annotated[int, Field(gt=0)]] = Field(None, exclude=True)


class RoomsPatchSchema(BasePatchSchema):
    hotel_id: int = None
    title: str = None
    description: str | None = None
    price: int = None
    quantity: int = None


class RoomsSchema(RoomsBaseSchema):
    id: int


class RoomsResponseSchema(BaseResponseSchema):
    data: list[RoomsSchema]
