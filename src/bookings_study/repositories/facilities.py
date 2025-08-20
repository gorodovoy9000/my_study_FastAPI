from bookings_study.models.facilities import FacilitiesOrm
from bookings_study.repositories.base import BaseRepository
from bookings_study.repositories.mappers.mappers import FacilitiesDataMapper


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    mapper = FacilitiesDataMapper
