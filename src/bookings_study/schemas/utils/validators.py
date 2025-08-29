def is_string_not_empty(value: str) -> str:
    if len(value) == 0:
        raise ValueError("This field cannot be empty")
    return value
