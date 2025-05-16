from pydantic import BaseModel

class HotelWriteScheme(BaseModel):
    name: str
    title: str


class HotelPatchScheme(BaseModel):
    name: str | None = None
    title: str | None = None


class HotelScheme(HotelWriteScheme):
    id: int

