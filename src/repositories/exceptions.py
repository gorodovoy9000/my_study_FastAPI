from src.exceptions import AppBaseException


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


# business logic exceptions
class RoomQuantityZeroOnDateIntervalException(AppBaseException):
    detail = "Room quantity is 0 on selected booking date interval"
