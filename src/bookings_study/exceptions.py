# base exception
class AppBaseException(Exception):
    detail = "Unexpected error"


# files exceptions
class FileAlreadyExistsException(AppBaseException):
    detail = "File already exists"


class FileNotFoundException(AppBaseException):
    detail = "File not found"
