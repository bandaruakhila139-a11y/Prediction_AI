import os
import sqlite3
from pathlib import Path
from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

DB_PATH = Path(__file__).resolve().parent / "projects.db"

def get_postgres_config(password=None):
    return {
        "host": os.environ.get("DB_HOST", "localhost"),
        "port": int(os.environ.get("DB_PORT", 5432)),
        "dbname": os.environ.get("DB_NAME", "ml_project"),
        "user": os.environ.get("DB_USER", "postgres"),
        "password": password if password is not None else os.environ.get("DB_PASSWORD", "")
    }

def test_postgres_connection(password=None):
    """
    Tests connection to PostgreSQL.
    Returns (True, message) if successful, (False, error_message) otherwise.
    """
    try:
        import psycopg2
    except ImportError:
        return False, "psycopg2 is not installed."
        
    cfg = get_postgres_config(password)
    if not cfg["password"]:
        return False, "PostgreSQL password not provided."
        
    # Try connecting to target db first
    try:
        conn = psycopg2.connect(
            host=cfg["host"],
            port=cfg["port"],
            user=cfg["user"],
            password=cfg["password"],
            dbname=cfg["dbname"],
            connect_timeout=3
        )
        conn.close()
        return True, f"Connected to PostgreSQL database '{cfg['dbname']}' successfully!"
    except psycopg2.OperationalError as e:
        err = str(e)
        if f'database "{cfg["dbname"]}" does not exist' in err:
            try:
                conn_maint = psycopg2.connect(
                    host=cfg["host"],
                    port=cfg["port"],
                    user=cfg["user"],
                    password=cfg["password"],
                    dbname="postgres",
                    connect_timeout=3
                )
                conn_maint.close()
                return True, f"Connected to PostgreSQL! ('{cfg['dbname']}' will be created automatically)."
            except Exception as e2:
                return False, str(e2).strip()
        return False, err.strip()
    except Exception as e:
        return False, str(e).strip()

def ensure_postgres_schema(password=None):
    """
    Ensures PostgreSQL database and 'projects' table exist.
    """
    import psycopg2
    cfg = get_postgres_config(password)
    
    try:
        conn = psycopg2.connect(
            host=cfg["host"],
            port=cfg["port"],
            user=cfg["user"],
            password=cfg["password"],
            dbname=cfg["dbname"],
            connect_timeout=3
        )
    except psycopg2.OperationalError as e:
        if f'database "{cfg["dbname"]}" does not exist' in str(e):
            conn_admin = psycopg2.connect(
                host=cfg["host"],
                port=cfg["port"],
                user=cfg["user"],
                password=cfg["password"],
                dbname="postgres",
                connect_timeout=3
            )
            conn_admin.autocommit = True
            with conn_admin.cursor() as cur:
                cur.execute(f'CREATE DATABASE "{cfg["dbname"]}"')
            conn_admin.close()
            
            conn = psycopg2.connect(
                host=cfg["host"],
                port=cfg["port"],
                user=cfg["user"],
                password=cfg["password"],
                dbname=cfg["dbname"],
                connect_timeout=3
            )
        else:
            raise e
            
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id SERIAL PRIMARY KEY,
                startup_name VARCHAR(150) NOT NULL,
                industry VARCHAR(100) NOT NULL,
                business_model VARCHAR(100) NOT NULL,
                target_market VARCHAR(150),
                budget NUMERIC(15,2),
                project_description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
    return conn

def save_project_to_postgres(project_data: dict, password=None) -> dict:
    conn = ensure_postgres_schema(password=password)
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO projects (startup_name, industry, business_model, target_market, budget, project_description)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (
            project_data.get("startup_name"),
            project_data.get("industry"),
            project_data.get("business_model"),
            project_data.get("target_market"),
            float(project_data.get("budget", 0) or 0),
            project_data.get("project_description", "")
        ))
        new_id = cur.fetchone()[0]
    conn.close()
    return {"source": "postgres", "success": True, "id": new_id}

def get_latest_project_from_postgres(password=None):
    try:
        conn = ensure_postgres_schema(password=password)
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, startup_name, industry, business_model, target_market, budget, project_description, created_at
                FROM projects
                ORDER BY id DESC
                LIMIT 1;
            """)
            row = cur.fetchone()
        conn.close()
        if row:
            return {
                "id": row[0],
                "startup_name": row[1],
                "industry": row[2],
                "business_model": row[3],
                "target_market": row[4],
                "budget": float(row[5]) if row[5] is not None else 0.0,
                "project_description": row[6],
                "created_at": str(row[7])
            }
    except Exception:
        pass
    return None

def is_supabase_configured() -> bool:
    url = os.environ.get("SUPABASE_URL", "").strip()
    key = os.environ.get("SUPABASE_KEY", "").strip()
    return bool(
        url and key and
        url.startswith("http") and
        "your-project" not in url and
        "your-anon" not in key
    )

def get_supabase_client():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not is_supabase_configured():
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in the .env file.")
    from supabase import create_client
    return create_client(url, key)

def init_sqlite_db():
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

def _save_to_sqlite(project_data: dict):
    init_sqlite_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO projects (startup_name, industry, business_model, target_market, budget, project_description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        project_data.get("startup_name"),
        project_data.get("industry"),
        project_data.get("business_model"),
        project_data.get("target_market"),
        float(project_data.get("budget", 0) or 0),
        project_data.get("project_description", "")
    ))
    conn.commit()
    conn.close()

def _get_latest_sqlite():
    try:
        init_sqlite_db()
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        if row:
            return dict(row)
    except Exception:
        pass
    return None

def save_project(project_data: dict, postgres_password=None) -> dict:
    """
    Primary: PostgreSQL (if password configured in .env or passed).
    Fallback: SQLite (with informative message).
    """
    pwd = postgres_password or os.environ.get("DB_PASSWORD", "")
    if pwd:
        try:
            return save_project_to_postgres(project_data, password=pwd)
        except Exception as e:
            _save_to_sqlite(project_data)
            return {"source": "postgres_error_fallback", "success": True, "error": str(e)}

    if is_supabase_configured():
        try:
            client = get_supabase_client()
            res = client.table("projects").insert({
                "startup_name": project_data.get("startup_name"),
                "industry": project_data.get("industry"),
                "business_model": project_data.get("business_model"),
                "target_market": project_data.get("target_market"),
                "budget": float(project_data.get("budget", 0) or 0),
                "project_description": project_data.get("project_description", "")
            }).execute()
            return {"source": "supabase", "success": True, "data": res.data}
        except Exception as e:
            _save_to_sqlite(project_data)
            return {"source": "sqlite_fallback", "success": True, "error": str(e)}

    # If no PostgreSQL password provided yet, save to SQLite and prompt user
    _save_to_sqlite(project_data)
    return {"source": "sqlite_no_postgres_pw", "success": True}

def get_latest_project(postgres_password=None):
    pwd = postgres_password or os.environ.get("DB_PASSWORD", "")
    if pwd:
        proj = get_latest_project_from_postgres(password=pwd)
        if proj:
            return proj
            
    if is_supabase_configured():
        try:
            client = get_supabase_client()
            res = client.table("projects").select("*").order("id", desc=True).limit(1).execute()
            if res.data and len(res.data) > 0:
                return res.data[0]
        except Exception:
            pass

    return _get_latest_sqlite()
