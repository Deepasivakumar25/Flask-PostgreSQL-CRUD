from flask import Flask, request, jsonify
from pydantic import BaseModel, EmailStr, ValidationError
from db import get_connection
from authentication import token_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import URL
from dotenv import load_dotenv
import os

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


class ProductCreation(BaseModel):
    product_name: str
    price: float
    category: str
    stock_quantity: int

class ProductUpdate(BaseModel):
    product_name: str
    price: float
    category: str
    stock_quantity: int

class ProductPatch(BaseModel):
    product_name: str | None = None
    price: float | None = None
    category: str | None = None
    stock_quantity: int | None = None

@app.route('/products', methods=['GET'])
def get_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM products""")
    products = cursor.fetchall() 
    cursor.close()
    conn.close()   
    return jsonify([{
        'id': product[0],
        'name': product[1],
        'price': product[2]
    } for product in products
    ]), 200

@app.route('/create_product', methods=['POST'])
@token_required
def create_product(employee_id):
    data = request.get_json()
    INSERT_PRODUCT_QUERY = """INSERT INTO products (product_name, price, category, stock_quantity) VALUES (%s, %s, %s, %s)"""
    conn= None
    cursor = None
    try:
        product_data = ProductCreation(**data)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(INSERT_PRODUCT_QUERY, (product_data.product_name, product_data.price, product_data.category, product_data.stock_quantity))
        result = {
            'message': 'Product created successfully',
            'product': {
                'name': product_data.product_name,
                'price': product_data.price,
                'category': product_data.category,
                'stock_quantity': product_data.stock_quantity
            }
        }
        conn.commit()
        return jsonify(result), 201
    
    except ValidationError as e:
        return jsonify({
            'message': 'Invalid input',
            'errors': e.errors()
        }), 400
    finally:
        if cursor:
           cursor.close()
        if conn:
           conn.close()

@app.route('/update_product/<int:product_id>', methods=['PUT'])
@token_required
def update_product(employee_id,product_id):
    data = request.get_json()
    UPDATE_PRODUCT_QUERY = """UPDATE products SET product_name = %s, price = %s, category = %s, stock_quantity = %s WHERE product_id = %s"""
    conn= None
    cursor = None
    try:
        product_data = ProductUpdate(**data)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(UPDATE_PRODUCT_QUERY, (product_data.product_name, product_data.price, product_data.category, product_data.stock_quantity, product_id))
        if cursor.rowcount == 0:
            return jsonify({'message': 'Product not found'}), 404
        result = {
            'message': 'Product updated successfully',
            'product': {
                'product_id': product_id,
                'product_name': product_data.product_name,
                'price': product_data.price,
                'category': product_data.category,
                'stock_quantity': product_data.stock_quantity
            }
        }
        conn.commit()
        return jsonify(result), 200

    except ValidationError as e:
        return jsonify({
            'message': 'Invalid input',
            'errors': e.errors()
        }), 400
    finally:
        if cursor:
           cursor.close()
        if conn:
           conn.close()

@app.route('/delete_product/<int:product_id>', methods=['DELETE'])
@token_required
def delete_product(employee_id,product_id):
    DELETE_PRODUCT_QUERY = """DELETE FROM products WHERE product_id = %s"""
    conn= None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(DELETE_PRODUCT_QUERY, (product_id,))
        if cursor.rowcount == 0:
            return jsonify({'message': 'Product not found'}), 404
        conn.commit()
        return jsonify({'message': 'Product deleted successfully'}), 200

    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500
    finally:
        if cursor:
           cursor.close()
        if conn:
           conn.close()

@app.route('/get_product/<int:product_id>', methods=['GET'])
@token_required
def get_product(employee_id, product_id):        
    SELECT_PRODUCT_QUERY = """SELECT * FROM products WHERE product_id = %s"""
    conn= None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(SELECT_PRODUCT_QUERY, (product_id,))
        product = cursor.fetchone()
        if not product:
            return jsonify({'message': 'Product not found'}), 404
        result = {
            'product_id': product[0],
            'product_name': product[1],
            'price': product[2],
            'category': product[3],
            'stock_quantity': product[4]
        }
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500
    finally:
        if cursor:
           cursor.close()
        if conn:
           conn.close()

@app.route('/partially_update_product/<int:product_id>', methods=['PATCH'])
@token_required
def partially_update_product(employee_id, product_id):
    data = request.get_json()
    UPDATE_PRODUCT_QUERY = """UPDATE products SET product_name = COALESCE(%s, product_name), price = COALESCE(%s, price), category = COALESCE(%s, category), stock_quantity = COALESCE(%s, stock_quantity) WHERE product_id = %s"""
    conn= None
    cursor = None
    try:
        product_data = ProductPatch(**data)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(UPDATE_PRODUCT_QUERY, (product_data.product_name, product_data.price, product_data.category, product_data.stock_quantity, product_id))
        if cursor.rowcount == 0:
            return jsonify({'message': 'Product not found'}), 404
        conn.commit()
        return jsonify({'message': 'Product updated successfully'}), 200

    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500
    finally:
        if cursor:
           cursor.close()
        if conn:
           conn.close()

#employees
class Department(db.Model):
    __tablename__ = 'departments'

    department_id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))

    employees = db.relationship(
        'Employee',
        back_populates='department'
    )

class Employee(db.Model):
    __tablename__ = 'employees'

    employee_id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)

    department_id = db.Column(
        db.Integer,
        db.ForeignKey('departments.department_id')
    )

    salary = db.Column(db.Float)
    hire_date = db.Column(db.Date)

    department = db.relationship(
        'Department',
        back_populates='employees'
    )

    def to_dict(self):
        return {
            'employee_id': self.employee_id,
            'employee_name': self.employee_name,
            'email': self.email,
            'department_id': self.department_id,
            'salary': self.salary,
            'hire_date': self.hire_date.isoformat() if self.hire_date else None
        }

@app.route('/sql_departments/<int:department_id>', methods=['GET'])
@token_required
def get_employees_by_department(employee_id,department_id):
    department = db.session.get(Department, department_id)

    if not department:
        return {'message': 'Department not found'}, 404

    return jsonify([
        employee.to_dict()
        for employee in department.employees
    ]), 200

@app.route('/sql_department_by_emp/<int:department_id>', methods=['GET'])
@token_required
def get_department(employee_id, department_id):

    department = db.session.get(Department, department_id)

    if not department:
        return {'message': 'Department not found'}, 404

    return {
        'department_id': department.department_id,
        'department_name': department.department_name,
        'location': department.location,
        'employees': [
            employee.to_dict()
            for employee in department.employees
        ]
    }, 200

if __name__ == '__main__':
    app.run(debug=True)

