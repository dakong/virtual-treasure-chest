from functools import wraps
from flask import session


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwds):
        if 'userID' in session:
            return fn(*args, **kwds)
        else:
            return (generateFailResponse({'message': 'Unauthorized'}), 401)

    return wrapper
