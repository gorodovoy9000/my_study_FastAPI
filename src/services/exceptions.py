from src.exceptions import AppBaseException


# auth exceptions
class InvalidPasswordException(AppBaseException):
    detail = "Invalid password"


class InvalidTokenException(AppBaseException):
    detail = "Invalid token"


class UserAlreadyExistsException(AppBaseException):
    detail = "User already exists"


class UserLoginFailedException(AppBaseException):
    detail = "User login failed"


# business entities exceptions
class FacilitiesInvalidException(AppBaseException):
    detail = "Facilities invalid"


class HotelHasRoomsException(AppBaseException):
    detail = "Hotel has remaining rooms"


class RoomHasBookingsException(AppBaseException):
    detail = "Room has remaining bookings"


class FacilityNotFoundException(AppBaseException):
    detail = "Facility not found"


class HotelNotFoundException(AppBaseException):
    detail = "Hotel not found"


class RoomNotFoundException(AppBaseException):
    detail = "Room not found"


class UserNotFoundException(AppBaseException):
    detail = "User not found"


# business logic exceptions
class DateFromBiggerOrEqualDateToException(AppBaseException):
    detail = "Field date_from is bigger or equal to field date_to"


class NoVacantRoomsException(AppBaseException):
    detail = "No vacant rooms on selected booking date interval"
