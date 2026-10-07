from flask import Flask, request, jsonify
from pydantic import BaseModel,EmailStr,ValidationError
from db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps

load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")

app = Flask(__name__)

class UserCreation(BaseModel):
    email: EmailStr
    password: str


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

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    INSERT_USER_QUERY = "INSERT INTO users (employee_id, email, password) VALUES (%s, %s, %s)"
    SELECT_USER_QUERY = "SELECT employee_id FROM users WHERE email = %s"

    try:
        user_data = UserCreation(**data)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(SELECT_USER_QUERY, (user_data.email,))
        existing_user = cursor.fetchone()
        if existing_user:
            cursor.close()
            conn.close()
            return jsonify({'message': 'User with this email already exists'}), 400
        hashed_password = generate_password_hash(user_data.password)
        cursor.execute(INSERT_USER_QUERY, (user_data.email, hashed_password))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'User registered successfully'}), 201
    except ValidationError as e:
        return jsonify({'errors': e.errors()}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    SELECT_USER_QUERY = "SELECT employee_id, email, password FROM users WHERE email = %s"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(SELECT_USER_QUERY, (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and check_password_hash(user[2], password):
        token = jwt.encode( { 'employee_id': user[0], 'exp': datetime.now(timezone.utc) + timedelta(hours=1) }, SECRET_KEY, algorithm='HS256' )
        return jsonify({'message': 'Login successful', 'token': token}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401

@app.route('/profile', methods=['GET'])
@token_required
def get_profile():
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return jsonify({'message': 'Authorization header is missing'}), 401

    token = auth_header.split(' ')[1]

    try:
        decoded_token = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=['HS256']
        )
        SELECT_USER_QUERY = "SELECT id, name, email FROM users WHERE id = %s"
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(SELECT_USER_QUERY,(decoded_token['user_id'],))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        return jsonify({
            'user_id': user[0],
            'name' : user[1],
            'email':user[2],
            'message': 'Token is valid',
        }), 200

    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401

    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401


if __name__ == '__main__':
    app.run(debug=True)