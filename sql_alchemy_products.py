from flask import request, jsonify
from sqlalchemy import or_
from auth_utils import token_required
from pydantic import BaseModel, ValidationError
from sqlalchemy.exc import SQLAlchemyError
from app import app, db

class ProductCreation(BaseModel):
    product_name: str
    price: float
    category: str
    stock_quantity: int

class Product(db.Model):
    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100))
    stock_quantity = db.Column(db.Integer)

@app.route('/sql_product/<int:product_id>', methods=['GET'])
@token_required
def get_sql_product(product_id):
    product = db.session.get(Product, product_id)

    if not product:
        return {'message': 'Product not found'}, 404

    return {
        'product_id': product.product_id,
        'product_name': product.product_name,
        'price': product.price,
        'category': product.category,
        'stock_quantity': product.stock_quantity
    }, 200

@app.route('/sql_products', methods=['GET'])
@token_required
def get_sql_products():
    products = Product.query.all()
    return [{
        'product_id': product.product_id,
        'product_name': product.product_name,
        'price': product.price,
        'category': product.category,
        'stock_quantity': product.stock_quantity
    } for product in products], 200

@app.route('/sql_create_product', methods=['POST'])
@token_required
def create_sql_product(employee_id):
    data = request.get_json()
    try:
        product_data = ProductCreation(**data)
        new_product = Product(
            product_name=product_data.product_name,
            price=product_data.price,
            category=product_data.category,
            stock_quantity=product_data.stock_quantity
        )
        db.session.add(new_product)
        db.session.flush()  # Flush to get the product_id of the new product    
        db.session.commit()

    except ValidationError as e:
        db.session.rollback()
        return {'errors': e.errors()}, 400

    except SQLAlchemyError as e:
        db.session.rollback()
        return {'message': 'Database error', 'error': str(e)}, 500

    return {
        'message': 'Product created successfully',
        'product_id': new_product.product_id
    }, 201

@app.route('/sql_update_product/<int:product_id>', methods=['PUT'])
@token_required
def update_sql_product(employee_id, product_id):
    data = request.get_json()
    product = db.session.get(Product, product_id)

    if not product:
        return {'message': 'Product not found'}, 404

    product.product_name = data.get('product_name', product.product_name)
    product.price = data.get('price', product.price)
    product.category = data.get('category', product.category)
    product.stock_quantity = data.get('stock_quantity', product.stock_quantity)

    db.session.commit()

    return {
        'message': 'Product updated successfully',
        'product_id': product.product_id
    }, 200

@app.route('/sql_delete_product/<int:product_id>', methods=['DELETE'])
@token_required
def delete_sql_product(employee_id, product_id):
    product = db.session.get(Product, product_id)

    if not product:
        return {'message': 'Product not found'}, 404

    db.session.delete(product)
    db.session.commit()

    return {'message': 'Product deleted successfully'}, 200

@app.route('/sql_partially_update_product/<int:product_id>', methods=['PATCH'])
@token_required
def partially_update_sql_product(employee_id, product_id):
    data = request.get_json()
    product = db.session.get(Product, product_id)

    if not product:
        return {'message': 'Product not found'}, 404

    for key, value in data.items():
        if hasattr(product, key):
            setattr(product, key, value)

    db.session.commit()

    return {
        'message': 'Product updated successfully',
        'product_id': product.product_id
    }, 200

#ORM Operations for Products table using SQLAlchemy
@app.route('/sql_products/<category>', methods=['GET'])
def get_sql_products_filter_by_category(category):
    #filter products by category and stock_quantity greater than 20 and order by price in ascending order using SQLAlchemy ORM
    products = Product.query.filter(Product.category == category,Product.stock_quantity > 100).order_by(Product.price.asc()).all()

    #filter products by category and stock_quantity greater than 20 and order by price in descending order using SQLAlchemy ORM
    # products = Product.query.filter(Product.category == category,Product.stock_quantity > 20).order_by(Product.price.desc()) 
    #   
    if not products:
        return {'message': 'No products found'}, 404
    return [{
        'product_id': product.product_id,
        'product_name': product.product_name,
        'price': product.price,
        'category': product.category,
        'stock_quantity': product.stock_quantity
    } for product in products], 200

#ORM OR and AND Operations for Products table using SQLAlchemy
@app.route('/sql_products_filter', methods=['GET'])
def get_sql_products_filter():
    #filter products by category and stock_quantity greater than 20 and order by price in ascending order using SQLAlchemy ORM
    products = Product.query.filter(or_(Product.category == 'Laptops',Product.category == 'Monitors'), Product.stock_quantity > 20).all()
    
    if not products:
        return {'message': 'No products found'}, 404
    
    return [{
        'product_id': product.product_id,
        'product_name': product.product_name,
        'price': product.price,
        'category': product.category,
        'stock_quantity': product.stock_quantity
    } for product in products], 200

#Get the count of products in a specific category using SQLAlchemy ORM  
@app.route('/count_sql_products/<category>', methods=['GET'])
def count_products_by_category(category):
    count = Product.query.filter(Product.category == category).count()
    return {'category': category, 'count': count}, 200
