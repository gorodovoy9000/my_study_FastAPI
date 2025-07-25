from src.repositories.bookings import BookingsRepository
from src.repositories.facilities import FacilitiesRepository
from src.repositories.hotels import HotelsRepository
from src.repositories.rooms import RoomsRepository
from src.repositories.users import UsersRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        # create session from factory
        self.session = self.session_factory()

        # add all repositories
        self.bookings = BookingsRepository(self.session)
        self.facilities = FacilitiesRepository(self.session)
        self.hotels = HotelsRepository(self.session)
        self.rooms = RoomsRepository(self.session)
        self.users = UsersRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
