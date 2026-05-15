# User Management API

A fast, lightweight, and modular User Management API built with **FastAPI**, **SQLite**, and **Pydantic**. 

This application allows you to create users, retrieve specific users by their ID, and filter users by their city, all with built-in data validation and easy-to-use endpoints.

## 🚀 Features

- **FastAPI Framework**: High performance and easy-to-use API framework.
- **SQLite Database**: Persistent, lightweight data storage using Python's built-in `sqlite3`.
- **Pydantic Validation**: Robust data validation and serialization for incoming and outgoing data.
- **Interactive Documentation**: Automatic interactive API documentation provided by Swagger UI and ReDoc.

## 📁 Project Structure

```
.
├── apiuser/
│   └── main.py       # Main FastAPI application and routing logic
├── users.db          # SQLite database (auto-generated)
├── requirements.txt  # Project dependencies
└── README.md         # Project documentation
```

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Navani06/apiuser.git
   cd apiuser
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Create a virtual environment
   python -m venv .venv
   
   # Activate it (Windows)
   .venv\Scripts\activate
   
   # Activate it (Mac/Linux)
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn pydantic python-dotenv
   ```

## 🏃‍♂️ Running the Application

To start the API server locally, run the following command from the root directory:

```bash
cd apiuser
uvicorn main:app --reload
```

The API will be running at `http://127.0.0.1:8000`.

## 📖 API Endpoints

### 1. Health Check
- **Endpoint**: `GET /`
- **Description**: Returns the health status of the API.

### 2. Create User
- **Endpoint**: `POST /users`
- **Description**: Creates a new user in the database.
- **Request Body**:
  ```json
  {
    "name": "John Doe",
    "age": 25,
    "email": "john@example.com",
    "city": "New York",
    "skills": ["Python", "FastAPI"]
  }
  ```

### 3. Get User by ID
- **Endpoint**: `GET /users/{user_id}`
- **Description**: Retrieves detailed information for a specific user.

### 4. Filter Users by City
- **Endpoint**: `GET /users?city={city_name}`
- **Description**: Retrieves a list of users filtered by the provided city query parameter. Example: `/users?city=Mumbai`.

## 📚 API Documentation

Once the server is running, you can access the automatically generated interactive API documentation:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
