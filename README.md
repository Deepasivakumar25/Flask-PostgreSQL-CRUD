# Flask PostgreSQL CRUD API

A Flask-based REST API project demonstrating CRUD operations with PostgreSQL, Pydantic request validation, JWT authentication, password hashing, and SQLAlchemy ORM.

## Project Overview

This project demonstrates how to build REST APIs using Flask with PostgreSQL.

It includes two approaches for database operations:

1. Direct PostgreSQL operations using `psycopg`
2. ORM-based database operations using Flask-SQLAlchemy and SQLAlchemy

The project also includes JWT-based authentication for protected API endpoints.

## Technologies Used

- Python
- Flask
- PostgreSQL
- psycopg
- Flask-SQLAlchemy
- SQLAlchemy
- Pydantic
- PyJWT
- Werkzeug
- python-dotenv

## Project Structure

```text
Flask-PostgreSQL-CRUD/
│
├── app.py
├── db.py
├── authentication.py
├── auth_utils.py
├── products.py
├── sql_alchemy_products.py
├── requirements.txt
├── .gitignore
└── README.md
```

### File Responsibilities

- `app.py` - Main Flask application, SQLAlchemy configuration, and application startup.
- `db.py` - PostgreSQL connection helper using `psycopg`.
- `authentication.py` - User registration, login, and profile APIs.
- `auth_utils.py` - JWT authentication and token validation utility.
- `products.py` - Product CRUD APIs using direct PostgreSQL queries with `psycopg`.
- `sql_alchemy_products.py` - Product APIs implemented using SQLAlchemy ORM.

## Features

### Product CRUD APIs

The project provides APIs for:

- Get all products
- Get a product by ID
- Create a product
- Update a product
- Partially update a product
- Delete a product

### Authentication

JWT authentication is implemented for protected endpoints.

Authentication features include:

- User registration
- User login
- Password hashing
- JWT token generation
- JWT token validation
- Token expiration handling
- Protected API endpoints

The JWT stores the authenticated employee ID and is used to identify the user for protected requests.

### PostgreSQL Integration

PostgreSQL is used as the application's database.

The project demonstrates two database access approaches:

**Direct PostgreSQL access**

`products.py` uses `psycopg` and SQL queries to perform CRUD operations.

**SQLAlchemy ORM**

`sql_alchemy_products.py` uses Flask-SQLAlchemy and SQLAlchemy models to perform database operations.

Database connection settings are loaded from environment variables.

### Pydantic Validation

Pydantic models are used to validate request data before database operations.

Validation is used for:

- User registration
- Product creation
- Product updates
- Partial product updates

### SQLAlchemy ORM

The SQLAlchemy implementation demonstrates:

- Defining database models
- Retrieving records by ID
- Querying records
- Filtering records
- Sorting records
- Counting records
- Using `or_()` conditions
- Working with relationships between tables

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

The `.gitignore` file excludes the `.env` file and Python virtual-environment directories.

## Installation

Clone the repository:

```bash
git clone https://github.com/Deepasivakumar25/Flask-PostgreSQL-CRUD.git
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

Create the required PostgreSQL database and tables used by the application.

For local development, configure the PostgreSQL connection details in the `.env` file.

The application uses the following database configuration variables:

- `DB_HOST`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_PORT`

## Running the Application

The project uses `app.py` as the single Flask application entry point.

Activate the virtual environment and run:

```powershell
flask --app app run --debug
```

The application will be available at:

```text
http://127.0.0.1:5000
```

You can also start the application directly with:

```powershell
python app.py
```

The application registers the authentication, direct PostgreSQL, and SQLAlchemy API routes when `app.py` starts.

## API Endpoints

### Authentication

```text
POST /register
POST /login
GET  /profile
```

### Product APIs - Direct PostgreSQL

These endpoints use `psycopg` and SQL queries.

```text
GET    /products
GET    /get_product/<product_id>
POST   /create_product
PUT    /update_product/<product_id>
PATCH  /partially_update_product/<product_id>
DELETE /delete_product/<product_id>
```

### Product APIs - SQLAlchemy

These endpoints use Flask-SQLAlchemy and SQLAlchemy ORM.

```text
GET    /sql_products
GET    /sql_product/<product_id>
POST   /sql_create_product
PUT    /sql_update_product/<product_id>
PATCH  /sql_partially_update_product/<product_id>
DELETE /sql_delete_product/<product_id>
```

Additional SQLAlchemy endpoints demonstrate category filtering, conditional filtering, and product counting:

```text
GET /sql_products/<category>
GET /sql_products_filter
GET /count_sql_products/<category>
```

The project also includes SQLAlchemy examples for querying department and employee relationships.

## Authentication Flow

### Register

A user registers with an employee ID, email, and password.

```text
POST /register
```

The application:

1. Validates the request using Pydantic.
2. Checks whether the email already exists.
3. Verifies that the employee ID exists.
4. Hashes the password using Werkzeug.
5. Stores the user in PostgreSQL.

### Login

A registered user sends their email and password:

```text
POST /login
```

Example request:

```json
{
    "email": "user@example.com",
    "password": "your_password"
}
```

After successful authentication, the API returns a JWT token.

### Accessing Protected Endpoints

The JWT must be sent in the `Authorization` header:

```text
Authorization: Bearer <JWT_TOKEN>
```

The token is validated before the protected endpoint is executed.

## Example HTTP Status Codes

The API uses standard HTTP status codes, including:

- `200 OK` - Successful request
- `201 Created` - Resource successfully created
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Missing or invalid authentication
- `404 Not Found` - Requested resource does not exist

## Learning Objectives

This project was created to practice and demonstrate:

- Flask REST API development
- HTTP methods and status codes
- CRUD operations
- PostgreSQL integration
- Direct database access with psycopg
- Pydantic request validation
- Password hashing
- JWT authentication
- Protected API endpoints
- SQLAlchemy ORM
- SQLAlchemy relationships
- Filtering and sorting with SQLAlchemy
- Environment variable management
- Backend API development

## Future Improvements

- Centralized error handling
- Automated tests
- API documentation
- Flask Blueprints
- Docker support
- PostgreSQL containerization
- Improved authentication and authorization
- Production configuration
