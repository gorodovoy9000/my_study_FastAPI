from sqlalchemy import select, insert
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    model: DeclarativeBase = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, **insert_data):
        stms = (
            insert(self.model)
            .values(**insert_data)
            .returning(self.model)
        )
        # debug stmt print
        # print(stms.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(stms)
        return result.scalars().first()
