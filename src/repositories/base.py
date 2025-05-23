from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    model: DeclarativeBase = None
    schema: BaseModel = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        model_objects = result.scalars().all()
        return [self.schema.model_validate(mo, from_attributes=True) for mo in model_objects]

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model_object = result.scalars().one()
        return self.schema.model_validate(model_object, from_attributes=True)

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model_object = result.scalars().one_or_none()
        if not model_object:
            return None
        return self.schema.model_validate(model_object, from_attributes=True)

    async def add(self, schema: BaseModel):
        stmt = (
            insert(self.model)
            .values(**schema.model_dump())
            .returning(self.model)
        )
        # debug stmt print
        # print(stms.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(stmt)
        model_object = result.scalars().one()
        return self.schema.model_validate(model_object, from_attributes=True)

    async def edit(self, schema: BaseModel, partial_update = False, **filter_by) -> None:
        # only one object allowed
        await self.get_one(**filter_by)
        stmt = (
            update(self.model)
            .values(**schema.model_dump(exclude_unset=partial_update))
            .filter_by(**filter_by)
        )
        await self.session.execute(stmt)

    async def delete(self, **filter_by) -> None:
        # only one object allowed
        await self.get_one(**filter_by)
        stmt = (
            delete(self.model)
            .filter_by(**filter_by)
        )
        await self.session.execute(stmt)
