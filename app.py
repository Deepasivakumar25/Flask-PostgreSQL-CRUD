import os

from flask import Flask,jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import URL
from dotenv import load_dotenv
from auth_utils import token_required

load_dotenv()

app = Flask(__name__)

database_url = URL.create(
    drivername="postgresql+psycopg",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME")
)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url

db = SQLAlchemy(app)

# Import routes after creating app and db
import authentication
import products
import sql_alchemy_products
import auth_utils

@app.route('/')
def home():
    return jsonify({
        'message': 'Flask API is running'
    })

if __name__ == '__main__':
    app.run(debug=True)