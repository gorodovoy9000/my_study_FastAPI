from datetime import date


# base exception
class AppBaseException(Exception):
    detail = "Unexpected error"


# db exceptions
class ManyFoundException(AppBaseException):
    detail = "Many objects were found"


class NotFoundException(AppBaseException):
    detail = "Objects are not found"


class NullValueException(AppBaseException):
    detail = "Null value found in not nullable column"


class ForeignKeyException(AppBaseException):
    detail = "Foreign key constraint violated"


class UniqueValueException(AppBaseException):
    detail = "Unique constraint violated"


# auth exceptions
class InvalidPasswordException(AppBaseException):
    detail = "Invalid password"


class InvalidTokenException(AppBaseException):
    detail = "Invalid token"


# files exceptions
class FileAlreadyExistsException(AppBaseException):
    detail = "File already exists"


class FileNotFoundException(AppBaseException):
    detail = "File not found"


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
class NoVacantRoomsException(AppBaseException):
    detail = "No vacant rooms remain"


class DateFromBiggerOrEqualDateToException(AppBaseException):
    detail = "Field date_from is bigger or equal to field date_to"


def validate_date_to_is_bigger_than_date_from(date_from: date, date_to: date):
    if date_from >= date_to:
        raise DateFromBiggerOrEqualDateToException
