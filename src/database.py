from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.config import settings


class Base(DeclarativeBase):
    pass


engine = create_async_engine(
    url=settings.DB_URL,
    echo=settings.DB_ECHO,
)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
