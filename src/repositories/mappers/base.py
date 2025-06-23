from abc import ABC

from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase


class BaseDataMapper(ABC):
    ModelOrmCls: type[DeclarativeBase]
    SchemaCls: type[BaseModel]

    @classmethod
    def map_to_domain_entity(cls, data: DeclarativeBase):
        return cls.SchemaCls.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, data: BaseModel):
        return cls.ModelOrmCls(**data.model_dump())
