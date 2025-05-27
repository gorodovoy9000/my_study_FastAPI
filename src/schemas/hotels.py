from pydantic import BaseModel, model_validator

class HotelWriteSchema(BaseModel):
    title: str
    location: str


class HotelPatchSchema(BaseModel):
    title: str | None = None
    location: str | None = None

    @model_validator(mode="before")
    def check_empty_data(cls, data):
        if not data:
            raise ValueError("empty data is not allowed")
        return data


class HotelSchema(HotelWriteSchema):
    id: int
