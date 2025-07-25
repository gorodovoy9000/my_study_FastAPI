from src.exceptions import AppBaseException
from src.repositories.exceptions import NotFoundException


# auth exceptions
class InvalidPasswordException(AppBaseException):
    detail = "Invalid password"


class InvalidTokenException(AppBaseException):
    detail = "Invalid token"


# business entities exceptions
class FacilitiesInvalidException(AppBaseException):
    detail = "Facilities invalid"


class RoomHasBookingsException(AppBaseException):
    detail = "Room has remaining bookings"


class HotelNotFoundException(NotFoundException):
    detail = "Hotel not found"


class RoomNotFoundException(NotFoundException):
    detail = "Room not found"


# business logic exceptions
class DateFromBiggerOrEqualDateToException(AppBaseException):
    detail = "Field date_from is bigger or equal to field date_to"


class NoVacantRoomsException(AppBaseException):
    detail = "No vacant rooms on selected booking date interval"
