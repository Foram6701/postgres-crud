from __future__ import annotations
import os
from typing import Optional, List

import psycopg
from psycopg import errors
from psycopg.rows import dict_row
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

def connect() -> Optional[psycopg.Connection]:
    """Open a DB connection using .env; return None on failure."""
    host = os.getenv("DB_HOST", "127.0.0.1")
    port = os.getenv("DB_PORT", "5432")
    user = os.getenv("DB_USER")
    db   = os.getenv("DB_NAME")
    pwd  = os.getenv("DB_PASSWORD")
    try:
        return psycopg.connect(
            host=host, port=port, user=user, dbname=db, password=pwd,
            row_factory=dict_row,
        )
    except Exception as e:
        print(f"Error connecting to the database ({host}:{port} as {user}): {e}")
        return None

# CRUD 
def get_all_students() -> Optional[List[dict]]:
    """Return all students ordered by id (or None if connection failed)."""
    conn = connect()
    if not conn:
        print("Could not connect; aborting SELECT.")
        return None
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT student_id, first_name, last_name, email, enrollment_date
                    FROM students
                    ORDER BY student_id;
                """)
                return cur.fetchall()
    finally:
        conn.close()

def add_student(first_name: str, last_name: str, email: str, enrollment_date: str) -> Optional[int]:
    """Insert a student; return new student_id, or None on failure (e.g., duplicate email)."""
    conn = connect()
    if not conn:
        print("Could not connect; aborting INSERT.")
        return None
    try:
        with conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                        INSERT INTO students (first_name, last_name, email, enrollment_date)
                        VALUES (%s, %s, %s, %s)
                        RETURNING student_id;
                    """, (first_name, last_name, email, enrollment_date))
                    return cur.fetchone()["student_id"]
                except errors.UniqueViolation:
                    print(f"Duplicate email: {email} (UNIQUE violation).")
                    return None
    finally:
        conn.close()

def update_student_email(student_id: int, new_email: str) -> bool:
    """Update email by id; return True iff exactly one row updated."""
    conn = connect()
    if not conn:
        print("Could not connect; aborting UPDATE.")
        return False
    try:
        with conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                        UPDATE students
                        SET email = %s
                        WHERE student_id = %s;
                    """, (new_email, student_id))
                    return cur.rowcount == 1
                except errors.UniqueViolation:
                    print(f"⚠️ Duplicate email: {new_email} (UNIQUE violation).")
                    return False
    finally:
        conn.close()

def delete_student(student_id: int) -> bool:
    """Delete by id; return True iff exactly one row deleted."""
    conn = connect()
    if not conn:
        print("Could not connect; aborting DELETE.")
        return False
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM students WHERE student_id = %s;", (student_id,))
                return cur.rowcount == 1
    finally:
        conn.close()

# print helper

def print_students(rows: Optional[List[dict]]) -> None:
    """Neatly print student rows."""
    if rows is None:
        print("(no data - connection issue)"); return
    if not rows:
        print("(no rows)"); return
    for r in rows:
        print(f"{r['student_id']} | {r['first_name']} {r['last_name']} | {r['email']} | {r['enrollment_date']}")

if __name__ == "__main__":
    print("=== TEST: get_all_students ===")
    print_students(get_all_students())
