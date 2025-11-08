# PostgreSQL CRUD (students)

Simple CRUD app against a `students` table using Python + psycopg (v3) and pgAdmin.

## Prerequisites
- Python 3.10+
- PostgreSQL running locally (my instance: host 127.0.0.1, port 5433)
- pgAdmin installed (for setup + demo)

## Database Setup
1. In pgAdmin: create DB **university**
2. Query Tool → run `db/setup.sql`
3. Verify:
   ```sql
   SELECT student_id, first_name, last_name, email, enrollment_date
   FROM students ORDER BY student_id;
