from flask import request, jsonify
import os
import jwt
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")


def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return jsonify({
                'message': 'Authorization header is missing'
            }), 401

        try:
            token = auth_header.split(' ')[1]

            decoded_token = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=['HS256']
            )

            employee_id = decoded_token['employee_id']

        except jwt.ExpiredSignatureError:
            return jsonify({
                'message': 'Token has expired'
            }), 401

        except (jwt.InvalidTokenError, IndexError, KeyError):
            return jsonify({
                'message': 'Invalid token'
            }), 401

        return f(employee_id, *args, **kwargs)

    return decorated