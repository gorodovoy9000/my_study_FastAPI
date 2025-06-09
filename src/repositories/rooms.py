from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.schemas.rooms import RoomsSchema

class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = RoomsSchema
