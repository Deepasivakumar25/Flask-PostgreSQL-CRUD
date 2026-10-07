from flask import request, jsonify
from pydantic import BaseModel,EmailStr,ValidationError
from app import app
from db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash
import os
import jwt
from auth_utils import token_required
from datetime import datetime, timedelta, timezone
from functools import wraps

SECRET_KEY = os.getenv("JWT_SECRET_KEY")

class UserCreation(BaseModel):
    employee_id: int
    email: EmailStr
    password: str

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    INSERT_USER_QUERY = """
        INSERT INTO users (employee_id, email, password)
        VALUES (%s, %s, %s)
    """

    SELECT_USER_QUERY = """
        SELECT employee_id
        FROM users
        WHERE email = %s
    """

    SELECT_EMPLOYEE_QUERY = """
        SELECT employee_id
        FROM employees
        WHERE employee_id = %s
    """

    try:
        user_data = UserCreation(**data)

        conn = get_connection()
        cursor = conn.cursor()

        # Check if email already exists
        cursor.execute(SELECT_USER_QUERY, (user_data.email,))
        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            conn.close()
            return jsonify({
                'message': 'User with this email already exists'
            }), 400

        # Check if employee ID exists
        cursor.execute(
            SELECT_EMPLOYEE_QUERY,
            (user_data.employee_id,)
        )

        employee = cursor.fetchone()

        if not employee:
            cursor.close()
            conn.close()
            return jsonify({
                'message': 'Invalid employee ID'
            }), 400

        # Hash password
        hashed_password = generate_password_hash(
            user_data.password
        )

        # Create user
        cursor.execute(
            INSERT_USER_QUERY,
            (
                user_data.employee_id,
                user_data.email,
                hashed_password
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            'message': 'User registered successfully'
        }), 201

    except ValidationError as e:
        return jsonify({
            'errors': e.errors()
        }), 400
    
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
def get_profile(employee_id):

    SELECT_USER_QUERY = """
        SELECT employee_id, email
        FROM users
        WHERE employee_id = %s
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        SELECT_USER_QUERY,
        (employee_id,)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user:
        return jsonify({
            'message': 'User not found'
        }), 404

    return jsonify({
        'employee_id': user[0],
        'email': user[1],
        'message': 'Token is valid'
    }), 200