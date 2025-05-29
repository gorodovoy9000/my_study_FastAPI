import re

# db exceptions
def parse_detail(err_text: str) -> str:
    match = re.search(r"\nDETAIL:(.*)\n", err_text)
    return match.group(1).strip()


class ManyFoundException(Exception):
    pass


class NotFoundException(Exception):
    pass


class NullValueException(Exception):
    pass


class ForeignKeyException(Exception):
    pass


class UniqueValueException(Exception):
    def __str__(self):
        return parse_detail(str(self.__context__))


# auth exceptions
class InvalidTokenException(Exception):
    pass
