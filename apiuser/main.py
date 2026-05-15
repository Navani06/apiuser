from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List
import sqlite3
import os
import json
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
            age     INTEGER NOT NULL,
            email   TEXT    NOT NULL DEFAULT '',
            city    TEXT    NOT NULL DEFAULT '',
            skills  TEXT    NOT NULL DEFAULT '[]'
        )
    """)
    
    # Check existing columns to apply migrations if needed
    cursor.execute("PRAGMA table_info(users)")
    columns = [col["name"] for col in cursor.fetchall()]
    
    if "email" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN email TEXT NOT NULL DEFAULT ''")
    if "city" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN city TEXT NOT NULL DEFAULT ''")
    if "skills" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN skills TEXT NOT NULL DEFAULT '[]'")

    conn.commit()
    conn.close()


init_db()


# ─── Pydantic Models ───────────────────────────────────────────────────────────

class UserCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, example="John Doe")
    age: int  = Field(..., gt=0, lt=150, example=25)
    email: str = Field(..., example="john@example.com")
    city: str = Field(..., example="New York")
    skills: List[str] = Field(..., example=["Python", "FastAPI"])


class UserResponse(BaseModel):
    id: int
    name: str
    age: int
    email: str
    city: str
    skills: List[str]


class UserDetailResponse(BaseModel):
    message: str
    user_name: str
    city: str
    total_skills: int
    user_data: UserResponse


class SuccessResponse(BaseModel):
    message: str
    user: UserResponse


class UserListResponse(BaseModel):
    message: str
    users: List[UserResponse]


# ─── Routes ────────────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
def root():
    """Health check endpoint."""
    return {"status": "running", "message": "Welcome to the User API with SQLite!"}


@app.post("/users", response_model=SuccessResponse, status_code=201, tags=["Users"])
def create_user(user: UserCreateRequest):
    """
    Create a new user and store in SQLite database.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (name, age, email, city, skills) VALUES (?, ?, ?, ?, ?)",
        (user.name, user.age, user.email, user.city, json.dumps(user.skills))
    )
    conn.commit()

    user_id = cursor.lastrowid
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    new_user = dict(cursor.fetchone())
    conn.close()

    new_user["skills"] = json.loads(new_user["skills"])

    return {
        "message": "User created successfully",
        "user": new_user
    }


@app.get("/users", response_model=UserListResponse, tags=["Users"])
def get_users_by_city(city: str = Query(..., description="Filter users by city")):
    """
    Filter users by city using query parameters.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE city = ?", (city,))
    rows = cursor.fetchall()
    conn.close()

    users = []
    for row in rows:
        user = dict(row)
        user["skills"] = json.loads(user["skills"])
        users.append(user)

    return {"message": "Users filtered successfully", "users": users}


@app.get("/users/{user_id}", response_model=UserDetailResponse, tags=["Users"])
def get_user(user_id: int):
    """
    Fetch a user by their ID from SQLite database.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user_row = cursor.fetchone()
    conn.close()

    if not user_row:
        raise HTTPException(
            status_code=404,
            detail=f"User with ID '{user_id}' not found."
        )

    user = dict(user_row)
    user["skills"] = json.loads(user["skills"])

    return {
        "message": "User fetched successfully",
        "user_name": user["name"],
        "city": user["city"],
        "total_skills": len(user["skills"]),
        "user_data": user
    }
