from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="User API",
    description="A simple FastAPI project to Create and Fetch Users using SQLite",
    version="2.0.0"
)

# ─── Database Setup ────────────────────────────────────────────────────────────
DB_PATH = os.getenv("DB_PATH", "users.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            name    TEXT    NOT NULL,
            age     INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()


init_db()


# ─── Pydantic Models ───────────────────────────────────────────────────────────

class UserCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, example="John Doe")
    age: int  = Field(..., gt=0, lt=150, example=25)


class UserResponse(BaseModel):
    id: int
    name: str
    age: int


class SuccessResponse(BaseModel):
    message: str
    user: UserResponse


# ─── Routes ────────────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
def root():
    """Health check endpoint."""
    return {"status": "running", "message": "Welcome to the User API with SQLite!"}


@app.post("/users", response_model=SuccessResponse, status_code=201, tags=["Users"])
def create_user(user: UserCreateRequest):
    """
    Create a new user and store in SQLite database.

    - **name**: Full name of the user (required)
    - **age**: Age of the user, must be between 1 and 149 (required)
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (name, age) VALUES (?, ?)",
        (user.name, user.age)
    )
    conn.commit()

    user_id = cursor.lastrowid
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    new_user = cursor.fetchone()
    conn.close()

    return {
        "message": "User created successfully",
        "user": dict(new_user)
    }


@app.get("/users/{user_id}", response_model=SuccessResponse, tags=["Users"])
def get_user(user_id: int):
    """
    Fetch a user by their ID from SQLite database.

    - **user_id**: The integer ID of the user
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User with ID '{user_id}' not found."
        )

    return {
        "message": "User fetched successfully",
        "user": dict(user)
    }
