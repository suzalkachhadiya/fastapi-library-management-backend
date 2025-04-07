# Library Management System

A FastAPI-based library management system that allows users to register, login, and manage book borrowing.

## Features

- User registration and authentication
- Book management (create, list, view details)
- Book borrowing and returning functionality
- Automatic book quantity management
- JWT-based authentication

## Prerequisites

- Python 3.8+
- PostgreSQL

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd library-management
```

2. Create a virtual environment and activate it:
```bash
python -m venv libraryenv
source libraryenv/bin/activate  # On Windows: libraryenv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL database:
   - Create a new database named `library_management`
   - Update the database URL in `src/app/config/database.py` if needed

5. Run the application:
```bash
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:
- Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## API Endpoints

### Users
- `POST /users/register` - Register a new user
- `POST /users/token` - Login and get access token
- `GET /users/me` - Get current user information

### Books
- `POST /books/` - Create a new book
- `GET /books/` - List all books
- `GET /books/{book_id}` - Get book details
- `POST /books/{book_id}/borrow` - Borrow a book
- `POST /books/{book_id}/return` - Return a book

## Authentication

The API uses JWT tokens for authentication. To access protected endpoints:
1. Register a user or login to get a token
2. Include the token in the Authorization header: `Bearer <token>`

## Database Schema

### Users Table
- user_id (Primary Key)
- username
- email
- password (hashed)

### Books Table
- book_id (Primary Key)
- book_name
- book_quantity

### Record Book Table
- record_id (Primary Key)
- user_id (Foreign Key)
- book_id (Foreign Key)
- borrowed_at
- submitted_at 