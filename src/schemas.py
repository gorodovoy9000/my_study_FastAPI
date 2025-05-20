from pydantic import BaseModel

class HotelWriteScheme(BaseModel):
    title: str
    location: str


class HotelPatchScheme(BaseModel):
    title: str | None = None
    location: str | None = None


class HotelScheme(HotelWriteScheme):
    id: int

