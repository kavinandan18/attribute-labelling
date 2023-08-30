from functools import wraps

import requests
from flask import current_app, g, jsonify, make_response, request


def verify_user():
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            bearer_token = request.headers.get("Authorization")
            if not bearer_token:
                return make_response(jsonify({"error": "Access token not found"}), 401)
            resp = requests.get(
                f"{current_app.config.get('UMP_URL')}/auth/user-permissions", headers={"Authorization": bearer_token}
            )
            json_resp = resp.json()
            if resp.status_code != 200:
                return make_response(jsonify(error=json_resp.get("error") or json_resp), resp.status_code)
            g.user_permissions = json_resp
            return f(*args, **kwargs)

        return wrapper

    return decorator
