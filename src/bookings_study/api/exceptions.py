from fastapi import HTTPException, status


class AppBaseHTTPException(HTTPException):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = ""

    def __init__(self):
        super().__init__(
            status_code=self.status_code,
            detail=self.detail,
        )


# files errors
class FilenameInvalidHTTPException(AppBaseHTTPException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = ("Invalid filename. "
              "Only allowed lower latin letters(a-z), digits, underscore(_) and optional extension after dot(.) "
              "Examples: file1.txt, some_image.jpg some_file etc")


class MediaFilenameInvalidHTTPException(AppBaseHTTPException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = ("Invalid media filename. "
              "Only allowed lower latin letters(a-z), digits, underscore(_) and extension after dot(.) "
              "Examples: image1.png, some_image.jpg etc")

# business logic exceptions
class BookingIsTooLongHTTPException(AppBaseHTTPException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "booking period is more than 180 days which is maximum"


class DateFromBiggerOrEqualDateToHTTPException(AppBaseHTTPException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "date_to must be bigger than date_from"


class FacilitiesInvalidHTTPException(AppBaseHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Facilities invalid"


# common not found exceptions
class NotFoundHTTPException(AppBaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND


class FacilityNotFoundHTTPException(NotFoundHTTPException):
    detail = "Facility not found"


class HotelNotFoundHTTPException(NotFoundHTTPException):
    detail = "Hotel not found"


class RoomNotFoundHTTPException(NotFoundHTTPException):
    detail = "Room not found"
