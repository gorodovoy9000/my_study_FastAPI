from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.schemas.bookings import BookingsSchema


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = BookingsSchema
