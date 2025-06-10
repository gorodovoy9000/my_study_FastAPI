from datetime import date

from pydantic import BaseModel


class BookingsBaseSchema(BaseModel):
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int


class BookingsRequestSchema(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingsWriteSchema(BookingsBaseSchema):
    pass


class BookingsSchema(BookingsBaseSchema):
    id: int
