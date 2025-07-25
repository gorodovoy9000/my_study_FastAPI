from datetime import date

from src.services.exceptions import DateFromBiggerOrEqualDateToException


def validate_date_to_is_bigger_than_date_from(date_from: date, date_to: date):
    if date_from >= date_to:
        raise DateFromBiggerOrEqualDateToException
