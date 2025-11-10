from __future__ import annotations
import os
from typing import Optional, List

import psycopg
from psycopg import errors
from psycopg.rows import dict_row
from dotenv import load_dotenv, find_dotenv

# Load environment variables from the nearest .env file.
load_dotenv(find_dotenv(), override=True)

def connect() -> Optional[psycopg.Connection]:
    """
    Open a PostgreSQL connection using credentials from environment variables.
    Returns:
        psycopg.Connection if successful, otherwise None (and prints a short error).
    Notes:
        - Uses psycopg3's dict_row to get rows as dicts (column_name -> value).
        - Defaults host/port if not provided; user/db/password must be present in env.
    """
    host = os.getenv("DB_HOST", "127.0.0.1")
    port = os.getenv("DB_PORT", "5432")
    user = os.getenv("DB_USER")
    db   = os.getenv("DB_NAME")
    pwd  = os.getenv("DB_PASSWORD")

    try:
        return psycopg.connect(
            host=host,
            port=port,
            user=user,
            dbname=db,
            password=pwd,
            row_factory=dict_row,  # return dict rows instead of tuples
        )
    except Exception as e:
        # Keep the message short but actionable; don’t leak secrets.
        print(f"Error connecting to the database ({host}:{port} as {user}): {e}")
        return None

# CRUD

def getAllStudents() -> Optional[List[dict]]:
    """
    Fetch all students ordered by student_id.
    Returns:
        List[dict] of rows like:
            {'student_id': ..., 'first_name': ..., 'last_name': ..., 'email': ..., 'enrollment_date': ...}
        or None if a connection could not be established.
    """
    conn = connect()
    if not conn:
        print("Could not connect; aborting SELECT.")
        return None
    try:
        # Using 'with conn:' ensures commit/rollback behavior
        with conn:
            # Cursor inherits dict row factory from connection.
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT student_id, first_name, last_name, email, enrollment_date
                    FROM students
                    ORDER BY student_id;
                """)
                return cur.fetchall()  # List[dict]
    finally:
        conn.close()  # Always close the connection.


def addStudent(first_name: str, last_name: str, email: str, enrollment_date: str) -> Optional[int]:
    """
    Insert a student and return the new student_id.
    Args:
        first_name, last_name, email, enrollment_date: basic fields for insert.
    Returns:
        int student_id on success; None on failure (e.g., duplicate email or connection failure).
    Notes:
        - Catches UniqueViolation (requires a UNIQUE constraint on email).
        - Uses server-side RETURNING to get the generated id.
    """
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
                    # Raised if email violates UNIQUE(email).
                    print(f"Duplicate email: {email} (UNIQUE violation).")
                    return None
    finally:
        conn.close()


def updateStudentEmail(student_id: int, new_email: str) -> bool:
    """
    Update a student's email by student_id.
    Returns:
        True if exactly one row was updated; False otherwise (including duplicate email violation).
    """
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
                    # rowcount is reliable for UPDATE/DELETE in psycopg3
                    return cur.rowcount == 1
                except errors.UniqueViolation:
                    # If email has a UNIQUE constraint and already exists elsewhere.
                    print(f"⚠️ Duplicate email: {new_email} (UNIQUE violation).")
                    return False
    finally:
        conn.close()


def deleteStudent(student_id: int) -> bool:
    """
    Delete a student by student_id.
    Returns:
        True iff exactly one row was deleted; False otherwise.
    """
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

# Printing helper

def printStudents(rows: Optional[List[dict]]) -> None:
    """
    Pretty-print student rows for quick debugging.
    Args:
        rows: output from getAllStudents() or similar.
    """
    if rows is None:
        print("(no data - connection issue)")
        return
    if not rows:
        print("(no rows)")
        return

    for r in rows:
        # Assume enrollment_date is directly printable (date or string).
        print(f"{r['student_id']} | {r['first_name']} {r['last_name']} | {r['email']} | {r['enrollment_date']}")


if __name__ == "__main__":
    print("=== TEST: get_all_students ===")
    printStudents(getAllStudents())
