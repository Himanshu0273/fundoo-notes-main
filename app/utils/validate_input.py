import re
from functools import wraps

from pydantic import ValidationError

from app.utils.exceptions import RegexValidationException


def regex_validator(field_name: str, pattern: str, error_msg: str):
    def decorator(func):
        @wraps(func)
        def wrapper(cls, value):
            if not re.fullmatch(pattern, value):
                raise RegexValidationException(field_name, error_msg)
            return func(cls, value)

        return wrapper

    return decorator


# RegEx Patterns
USERNAME_REGEX = r"^[a-z][a-z0-9]{3,}$"
PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
