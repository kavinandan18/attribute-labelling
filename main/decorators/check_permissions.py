from copy import deepcopy
from functools import wraps

from flask import current_app, g, jsonify, make_response


def verify_permissions(permissions_to_check: dict, match_all: bool = False):
    """
    To verify the user permissions.
    :param permissions_to_check:
    :param match_all:
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            permissions = deepcopy(permissions_to_check)
            for permission in g.user_permissions:
                if permission["application"] == current_app.config.get("APPLICATION_NAME"):
                    if (
                        permissions.get(permission.get("model"))
                        and permission["permission"] in permissions[permission["model"]]
                    ):
                        permissions[permission["model"]].remove(permission["permission"])
                        if not permissions[permission["model"]]:
                            del permissions[permission["model"]]
                        if not match_all or not permission:
                            break
            else:
                return make_response(jsonify(error="Unauthorized User"), 401)

            if match_all and permissions:
                return make_response(jsonify(error="Unauthorized User"), 401)
            return f(*args, **kwargs)

        return wrapper

    return decorator
