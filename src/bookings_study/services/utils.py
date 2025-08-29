from datetime import date

from bookings_study.services.exceptions import BookingIsTooLongException, DateFromBiggerOrEqualDateToException


def validate_date_to_is_bigger_than_date_from(date_from: date, date_to: date):
    if date_from >= date_to:
        raise DateFromBiggerOrEqualDateToException


def validate_booking_length(date_from: date, date_to: date):
    td = date_to - date_from
    if td.days > 180:
        raise BookingIsTooLongException
