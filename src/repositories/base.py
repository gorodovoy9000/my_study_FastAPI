from psycopg.errors import ForeignKeyViolation, NotNullViolation, UniqueViolation
from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import IntegrityError, MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import (
    ForeignKeyException, ManyFoundException, NullValueException,
    NotFoundException, UniqueValueException,
)


class BaseRepository:
    model: DeclarativeBase = None
    schema: BaseModel = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, *args, **kwargs):
        # build query
        query = select(self.model)
        # execute
        result = await self.session.execute(query)
        model_objects = result.scalars().all()
        return [self.schema.model_validate(mo, from_attributes=True) for mo in model_objects]

    async def get_one(self, **filter_by):
        # build query
        query = select(self.model).filter_by(**filter_by)
        # execute and check about none or many objects found
        try:
            result = await self.session.execute(query)
            model_object = result.scalars().one()
        except NoResultFound as err:
            raise NotFoundException(err)
        except MultipleResultsFound as err:
            raise ManyFoundException(err)
        return self.schema.model_validate(model_object, from_attributes=True)

    async def get_one_or_none(self, **filter_by):
        # build query
        query = select(self.model).filter_by(**filter_by)
        # execute and check about none or many objects found
        try:
            result = await self.session.execute(query)
            model_object = result.scalars().one_or_none()
        except NoResultFound as err:
            raise NotFoundException(err)
        except MultipleResultsFound as err:
            raise ManyFoundException(err)
        # return None or schema
        if not model_object:
            return None
        return self.schema.model_validate(model_object, from_attributes=True)

    async def add(self, schema: BaseModel):
        # build insert statement
        stmt = (
            insert(self.model)
            .values(**schema.model_dump())
            .returning(self.model)
        )
        # debug stmt print
        # print(stms.compile(engine, compile_kwargs={"literal_binds": True}))
        try:
            result = await self.session.execute(stmt)
            model_object = result.scalars().one()
        # execute and check about constrain violations
        except IntegrityError as err:
            if isinstance(err.__context__, ForeignKeyViolation):
                raise ForeignKeyException(err)
            elif isinstance(err.__context__, NotNullViolation):
                raise NullValueException(err)
            elif isinstance(err.__context__, UniqueViolation):
                raise UniqueValueException(err)
        return self.schema.model_validate(model_object, from_attributes=True)

    async def edit(self, schema: BaseModel, partial_update = False, **filter_by) -> None:
        # only one object allowed
        await self.get_one(**filter_by)
        # build update statement
        stmt = (
            update(self.model)
            .values(**schema.model_dump(exclude_unset=partial_update))
            .filter_by(**filter_by)
        )
        # execute and check about constrain violations
        try:
            await self.session.execute(stmt)
        except IntegrityError as err:
            if isinstance(err.__context__, ForeignKeyViolation):
                raise ForeignKeyException(err)
            elif isinstance(err.__context__, NotNullViolation):
                raise NullValueException(err)
            elif isinstance(err.__context__, UniqueViolation):
                raise UniqueValueException(err)

    async def delete(self, **filter_by) -> None:
        # only one object allowed
        await self.get_one(**filter_by)
        # build delete statement
        stmt = (
            delete(self.model)
            .filter_by(**filter_by)
        )
        try:
            await self.session.execute(stmt)
        except IntegrityError as err:
            if isinstance(err.__context__, ForeignKeyViolation):
                raise ForeignKeyException(err)
