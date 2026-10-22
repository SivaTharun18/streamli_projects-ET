import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager


@contextmanager
def get_connection():
    conn = None

    try:
        config = st.secrets["postgres"]

        if config.get("url"):
            conn = psycopg2.connect(
                config["url"],
                cursor_factory=RealDictCursor
            )
        else:
            conn = psycopg2.connect(
                host=config["host"],
                port=config["port"],
                database=config["database"],
                user=config["user"],
                password=config["password"],
                cursor_factory=RealDictCursor
            )

        yield conn
        conn.commit()

    except Exception:
        if conn:
            conn.rollback()
        raise

    finally:
        if conn:
            conn.close()


def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)


def create_user(username, email, password_hash):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO users
                    (username, email, password_hash)
                    VALUES (%s, %s, %s)
                """, (username, email, password_hash))

        return True

    except psycopg2.errors.UniqueViolation:
        return False


def get_user_by_username(username):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM users WHERE username = %s",
                (username,)
            )
            return cur.fetchone()


def get_all_users():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, username, email, created_at
                FROM users
                ORDER BY id
            """)
            return cur.fetchall()


def user_exists(username=None, email=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            if username:
                cur.execute(
                    "SELECT 1 FROM users WHERE username = %s",
                    (username,)
                )
            elif email:
                cur.execute(
                    "SELECT 1 FROM users WHERE email = %s",
                    (email,)
                )
            else:
                return False

            return cur.fetchone() is not None