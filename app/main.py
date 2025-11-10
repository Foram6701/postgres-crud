from app.db_access import (
    getAllStudents,
    addStudent,
    updateStudentEmail,
    deleteStudent,
    printStudents,
)

def demo_sequence():
    """
    Run a simple CRUD demo:
      1) Show current rows
      2) Insert a student and show rows
      3) Update a student's email and show rows
      4) Delete that student and show rows
    """
    # 1) BEFORE — list all students currently in the table.
    print("=== BEFORE ===")
    printStudents(getAllStudents())

    # 2) INSERT — add a new student; show rows afterward.
    print("\n=== INSERT ===")
    new_id = addStudent("Alice", "Brown", "alice.brown@example.com", "2023-09-03")
    print(f"Inserted id={new_id}")

    print("\n=== AFTER INSERT ===")
    printStudents(getAllStudents())

    # 3) UPDATE — update email for a specific student_id.
    updated = updateStudentEmail(16, "alice.updated@example.com")
    print(f"Updated={updated}")

    print("\n=== AFTER UPDATE ===")
    printStudents(getAllStudents())

    # 4) DELETE — delete by id and show rows afterward.
    print("\n=== DELETE ===")
    deleted = deleteStudent(16)
    print(f"Deleted={deleted}")

    print("\n=== AFTER DELETE ===")
    printStudents(getAllStudents())

if __name__ == "__main__":
    # Entry point for running the demo directly.
    demo_sequence()
