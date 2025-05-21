from src.models import RoomsOrm
from repositories.base import BaseRepository


class RoomsRepository(BaseRepository):
    model = RoomsOrm
