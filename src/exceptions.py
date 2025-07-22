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


# business logic exceptions
class NoVacantRoomsException(AppBaseException):
    detail = "No vacant rooms remain"
