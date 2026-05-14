# 👤 User API — FastAPI + SQLite

A simple REST API built with **FastAPI** and **SQLite** to create and fetch users.

---

## 📁 Project Structure

```
user_api/
├── main.py           # All API routes and logic
├── requirements.txt  # Python dependencies
├── .env              # Environment variables
├── .gitignore        # Files to ignore in Git
├── git_push.sh       # Push script for Mac/Linux
├── git_push.bat      # Push script for Windows
└── README.md         # Project documentation
```

> `users.db` is auto-created when you run the server for the first time.

---

## ⚙️ Setup Instructions

### 1. Create and activate virtual environment

```bash
python -m venv venv
```

- **Windows:** `venv\Scripts\activate`
- **Mac/Linux:** `source venv/bin/activate`

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the server

```bash
uvicorn main:app --reload
```

Server starts at: **http://127.0.0.1:8000**

---

## 📬 API Endpoints

### ✅ Health Check
```
GET /
```

### ➕ Create a User
```
POST /users
```
**Request Body:**
```json
{
  "name": "John Doe",
  "age": 25
}
```
**Response (201):**
```json
{
  "message": "User created successfully",
  "user": { "id": 1, "name": "John Doe", "age": 25 }
}
```

### 🔍 Get User by ID
```
GET /users/{user_id}
```
**Response (200):**
```json
{
  "message": "User fetched successfully",
  "user": { "id": 1, "name": "John Doe", "age": 25 }
}
```
**Error (404):**
```json
{
  "detail": "User with ID '99' not found."
}
```

---

## 🧪 Test via Swagger UI

Open: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📝 Notes

- SQLite database file `users.db` is created automatically on first run.
- No extra database installation needed — SQLite is built into Python.
- IDs are auto-incremented integers (1, 2, 3...).
