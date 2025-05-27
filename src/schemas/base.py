from pydantic import BaseModel, model_validator


class BasePatchSchema(BaseModel):
    @model_validator(mode="before")
    def check_empty_data(cls, data):
        if not data:
            raise ValueError("empty data is not allowed")
        return data
