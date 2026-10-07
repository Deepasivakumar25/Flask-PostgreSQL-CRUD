# Flask PostgreSQL CRUD API

A Flask-based REST API project demonstrating CRUD operations, JWT authentication, PostgreSQL database integration, Pydantic validation, and SQLAlchemy ORM.

## Project Overview

This project contains REST API implementations using Flask and PostgreSQL.

It demonstrates two approaches for working with PostgreSQL:

1. Direct database operations using `psycopg`
2. Database operations using Flask-SQLAlchemy and SQLAlchemy ORM

The project also includes JWT-based authentication to protect API endpoints.

## Technologies Used

* Python
* Flask
* PostgreSQL
* psycopg
* Flask-SQLAlchemy
* SQLAlchemy
* Pydantic
* PyJWT
* Werkzeug
* python-dotenv

## Project Structure

```text
Flask-PostgreSQL-CRUD/
│
├── products.py
├── authentication.py
├── sql_alchemy_products.py
├── db.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Features

### Product APIs

The project provides APIs for:

* Get all products
* Get a product by ID
* Create a product
* Update a product
* Partially update a product
* Delete a product

### Authentication

JWT authentication is implemented for protected endpoints.

Authentication features include:

* User registration
* User login
* Password hashing
* JWT token generation
* JWT token validation
* Token expiration handling
* Protected API endpoints

### PostgreSQL Integration

The project uses PostgreSQL as the database.

Database connection details are loaded using environment variables.

The `db.py` module uses `psycopg` to establish database connections.

### Pydantic Validation

Pydantic models are used to validate request data before performing database operations.

Examples include:

* Product creation validation
* Product update validation
* Partial product update validation
* User registration validation

### SQLAlchemy ORM

The project also demonstrates database operations using Flask-SQLAlchemy.

SQLAlchemy examples include:

* Creating models
* Retrieving records by ID
* Querying all records
* Filtering records
* Sorting records
* Counting records
* Using `or_()` conditions
* Working with relationships between tables

## Environment Variables

Create a `.env` file in the project directory.

```text
DB_HOST=localhost
DB_NAME=company_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432

JWT_SECRET_KEY=your_secret_key
```

Do not commit the `.env` file to GitHub.

## Installation

Clone the repository:

```bash
git clone <repository-url>
```

Navigate to the project directory:

```bash
cd Flask-PostgreSQL-CRUD
```

Create a virtual environment:

```bash
python -m venv fenv
```

Activate the virtual environment on Windows:

```powershell
fenv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Database Setup

Create a PostgreSQL database and configure the required database tables.

Update the `.env` file with your PostgreSQL connection details.

## Running the Application

Run the Flask application:

```bash
python products.py
```

The application will start on:

```text
http://127.0.0.1:5000
```

The authentication API can be run separately using:

```bash
python authentication.py
```

The SQLAlchemy product API can be run using:

```bash
python sql_alchemy_products.py
```

## Example API Endpoints

### Authentication

```text
POST /register
POST /login
GET  /profile
```

### Product APIs

```text
GET    /products
GET    /get_product/<product_id>
POST   /create_product
PUT    /update_product/<product_id>
PATCH  /partially_update_product/<product_id>
DELETE /delete_product/<product_id>
```

### SQLAlchemy Product APIs

```text
GET    /sql_products
GET    /sql_product/<product_id>
POST   /sql_create_product
PUT    /sql_update_product/<product_id>
PATCH  /sql_partially_update_product/<product_id>
DELETE /sql_delete_product/<product_id>
```

Additional SQLAlchemy ORM examples demonstrate filtering, sorting, counting, and conditional queries.

## Authentication

Protected endpoints require a JWT token in the `Authorization` header.

Example:

```text
Authorization: Bearer <JWT_TOKEN>
```

A token is generated after successful login and must be provided when accessing protected endpoints.

## Learning Objectives

This project was created to practice and demonstrate:

* Flask REST API development
* HTTP methods and status codes
* CRUD operations
* PostgreSQL integration
* Database connection handling
* Pydantic request validation
* Password hashing
* JWT authentication
* SQLAlchemy ORM
* SQLAlchemy relationships
* Filtering and sorting with SQLAlchemy
* Environment variable management
* Backend API development

## Future Improvements

* Add centralized error handling
* Add API documentation
* Improve project structure using Flask Blueprints
* Add automated tests
* Add Docker support
* Add PostgreSQL containerization
* Improve authentication and authorization
* Add production configuration
