from abc import ABC

from pydantic import BaseModel

from src.database import Base


class BaseDataMapper(ABC):
    ModelOrmCls: type[Base]
    SchemaCls: type[BaseModel]

    @classmethod
    def map_to_domain_entity(cls, data: Base):
        return cls.SchemaCls.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, data: BaseModel):
        return cls.ModelOrmCls(**data.model_dump())
