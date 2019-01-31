
from functools import wraps
from flask import jsonify, request, make_response
from jsonschema import validate, ValidationError


def validate_payload_is_json(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not request.json:
            msg = "payload is not json"
            return make_response(jsonify({"message": msg}), 400)
        return func(*args, **kwargs)
    return wrapper

def validate_payload_with_schema(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                validate(instance=request.json, schema=schema)
            except ValidationError as e:
                msg = e.message
                return make_response(jsonify({"message": msg}), 400)
            return func(*args, **kwargs)
        return wrapper
    return decorator