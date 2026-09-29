import os
import sqlite3
from pathlib import Path

# Database file stored in the project folder
DB_PATH = Path(__file__).resolve().parent / "projects.db"

def init_db():
    """Initializes the database and ensures the projects table exists."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            startup_name TEXT NOT NULL,
            industry TEXT NOT NULL,
            business_model TEXT NOT NULL,
            target_market TEXT,
            budget REAL,
            project_description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_project(project_data: dict) -> dict:
    """
    Saves a startup project record directly to the database.
    """
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO projects (startup_name, industry, business_model, target_market, budget, project_description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        project_data.get("startup_name", "").strip(),
        project_data.get("industry", "").strip(),
        project_data.get("business_model", "").strip(),
        project_data.get("target_market", "").strip(),
        float(project_data.get("budget", 0) or 0),
        project_data.get("project_description", "").strip()
    ))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {"success": True, "id": new_id}

def get_latest_project() -> dict | None:
    """
    Retrieves the most recent project submission from the database.
    """
    try:
        init_db()
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        if row:
            return dict(row)
    except Exception as e:
        print(f"Database query error: {e}")
    return None

def get_all_projects() -> list:
    """
    Retrieves all submitted projects from the database.
    """
    try:
        init_db()
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception as e:
        print(f"Database query error: {e}")
        return []
