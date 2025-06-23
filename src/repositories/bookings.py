from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingsDataMapper


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingsDataMapper
