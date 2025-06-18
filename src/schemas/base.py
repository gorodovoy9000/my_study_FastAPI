from pydantic import BaseModel, ConfigDict, model_validator


class BasePatchSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="before")
    def check_empty_data(cls, data):
        if not data:
            raise ValueError("empty data is not allowed")
        return data
