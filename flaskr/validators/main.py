from .. import wraps
from .. import jsonify
from .. import request
from .. import validate
from .. import wraps
from .. import ValidationError


def validate_json(f):
    """
    The decorator to validate the json
    """
    @wraps(f)
    def wrapper(*args, **kw):
        request.json

        return f(*args, **kw)

    return wrapper


def validate_schema(schema):
    """
    Validate the json data passed by request
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            validate(request.json, schema)

            return f(*args, **kw)

        return wrapper

    return decorator
