from fastapi import HTTPException, status


class AppBaseHTTPException(HTTPException):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = ""

    def __init__(self):
        super().__init__(
            status_code=self.status_code,
            detail=self.detail,
        )


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
