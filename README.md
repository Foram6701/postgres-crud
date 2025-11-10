PostgreSQL CRUD App (Python + psycopg3):

A minimal Python application demonstrating **CRUD (Create, Read, Update, Delete)** operations on a PostgreSQL database using `psycopg3` and environment variables.  

Project Structure:
Main Folder: postgres-crud
Sub-Folder 1: db
Files:
setup.sql
all_queries.sql

Sub-Folder 2: app
Files:
db_access.py
main.py

Other Files:
README.md
requirements.txt
.env

Setup Instructions:

1. Clone the repository:
Commands:
git clone https://github.com/<your-username>/postgres-crud.git
cd postgres-crud

2. Create and activate a virtual environment:
Commands:
python3 -m venv .venv
source .venv/bin/activate   # macOS/Linux
OR
.venv\Scripts\activate      # Windows

3. Install dependencies:
pip install -r requirements.txt

4. Environment Variables:

Create a `.env` file in the project root (or copy from the example) with this command:
cp .env.example .env

Then open `.env` and fill in your real database credentials:
DB_NAME=university
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=127.0.0.1
DB_PORT=5433

Database Setup:

1. Open pgAdmin or run psql and connect to your PostgreSQL server.
2. Create new database names university using the following query:

CREATE DATABASE university;
3. Run the setup.sql file:
   a. Right-click university database in pgAdmin -> "Query Tool". Click "Open File" -> select setup.sql. Click Execute.
   b. Run the following command in Terminal:
      psql -U postgres -d university -f setup.sql


Running the App:

Run the program from the project root with this command:

python -m app.main

You should see output like:
=== BEFORE ===
1 | John Doe | john.doe@example.com | 2023-09-01
2 | Jane Smith | jane.smith@example.com | 2023-09-01
3 | Jim Beam | jim.beam@example.com | 2023-09-02

=== INSERT ===
Inserted id=6

=== AFTER INSERT ===
1 | John Doe | john.doe@example.com | 2023-09-01
2 | Jane Smith | jane.smith@example.com | 2023-09-01
3 | Jim Beam | jim.beam@example.com | 2023-09-02
6 | Alice Brown | alice.brown@example.com | 2023-09-03

Dependencies:

Install them manually if needed with this command:
pip install "psycopg[binary]" python-dotenv

Demo Video:
https://youtu.be/DFomGYDqIXI
