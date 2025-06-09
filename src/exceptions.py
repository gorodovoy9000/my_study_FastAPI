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
    def __str__(self):
        return parse_detail(str(self.__context__))


class ForeignKeyException(Exception):
    def __str__(self):
        return parse_detail(str(self.__context__))


class UniqueValueException(Exception):
    def __str__(self):
        return parse_detail(str(self.__context__))


# auth exceptions
class InvalidPasswordException(Exception):
    pass


class InvalidTokenException(Exception):
    pass
