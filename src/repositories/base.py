from abc import ABC

from psycopg.errors import ForeignKeyViolation, NotNullViolation, UniqueViolation
from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update, Table
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import IntegrityError, MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import (
    ForeignKeyException, ManyFoundException, NullValueException,
    NotFoundException, UniqueValueException,
)
from src.repositories.mappers.base import BaseDataMapper


class BaseRepository(ABC):
    model: DeclarativeBase
    mapper: BaseDataMapper

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_many_filtered(self, *filters, limit=100, offset=0, **filter_by):
        # build query with filters
        query = (
            select(self.model)
            .filter(*filters)
            .filter_by(**filter_by)
        )
        # pagination
        query = query.limit(limit).offset(offset)
        # execute
        result = await self.session.execute(query)
        model_objects = result.scalars().all()
        return [self.mapper.map_to_domain_entity(mo) for mo in model_objects]

    async def get_all(self):
        return await self.get_many_filtered()

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
        return self.mapper.map_to_domain_entity(model_object)

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
        return self.mapper.map_to_domain_entity(model_object)

    async def add(self, in_data: BaseModel):
        # build insert statement
        stmt = (
            insert(self.model)
            .values(**in_data.model_dump())
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
        return self.mapper.map_to_domain_entity(model_object)

    async def add_bulk(self, bulk_data: list[BaseModel]):
        stmt = insert(self.model).values([d.model_dump() for d in bulk_data])
        await self.session.execute(stmt)

    async def edit(self, in_data: BaseModel, partial_update = False, **filter_by) -> None:
        # only one object allowed
        await self.get_one(**filter_by)
        # build update statement
        stmt = (
            update(self.model)
            .values(**in_data.model_dump(exclude_unset=partial_update))
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
        # execute and check about constrain violations
        try:
            await self.session.execute(stmt)
        except IntegrityError as err:
            if isinstance(err.__context__, ForeignKeyViolation):
                raise ForeignKeyException(err)


class BaseM2MRepository(ABC):
    table: Table

    def __init__(self, session: AsyncSession, main_column_name: str, target_column_name: str):
        self.session = session
        self.main_column_name = main_column_name
        self.main_column = getattr(self.table.c, self.main_column_name)
        self.target_column_name = target_column_name
        self.target_column = getattr(self.table.c, self.target_column_name)

    async def add(self, main_obj_id: int, target_objs_ids: list[int]):
        """Add target objects to the main object"""
        # form rows to add dict
        rows_to_add = [
            {
                self.main_column_name: main_obj_id,
                self.target_column_name: o_id,
            } for o_id in target_objs_ids
        ]
        # build and execute statement
        stmt = insert(self.table).values(rows_to_add)
        await self.session.execute(stmt)

    async def delete(self, main_obj_id: int, target_objs_ids: list[int]):
        """Delete target objects by their ids only linked to the main object"""
        # form filters to delete rows
        filters = [
            self.main_column == main_obj_id,
            self.target_column.in_(target_objs_ids),
        ]
        # build and execute statement
        stmt = delete(self.table).filter(*filters)
        await self.session.execute(stmt)

    async def edit(self, main_obj_id: int, target_objs_ids: list[int]):
        """Edit only changed objects - add not existing, delete missing, do nothing with not changed"""
        # select db target objects and prepare sets
        db_m2m_ids = set(await self.select(main_obj_id))
        given_m2m_ids = set(target_objs_ids)
        # compare given and db objects ids - form to add and to delete
        to_delete_m2m_ids = db_m2m_ids - given_m2m_ids
        to_add_m2m_ids = given_m2m_ids - db_m2m_ids
        # delete m2m objects
        if to_delete_m2m_ids:
            await self.delete(main_obj_id, list(to_delete_m2m_ids))
        # add m2m objects
        if to_add_m2m_ids:
            await self.add(main_obj_id, list(to_add_m2m_ids))

    async def select(self, main_obj_id: int):
        """Select all objects linked to main"""
        query = select(self.target_column).filter(self.main_column == main_obj_id)
        result = await self.session.execute(query)
        return result.scalars().all()
