"""
main.py
-------
Demo runner that calls the CRUD functions in a clear sequence,
printing results that are easy to show in your video.
"""

from app.db_access import (
    get_all_students,
    add_student,
    update_student_email,
    delete_student,
    print_students,
)


def demo_sequence():
    # 1) BEFORE
    print("=== BEFORE ===")
    print_students(get_all_students())

    # 2) INSERT
    print("\n=== INSERT ===")
    new_id = add_student("Alice", "Brown", "alice.brown@example.com", "2023-09-03")
    print(f"Inserted id={new_id}")
    print("\n=== AFTER INSERT ===")
    print_students(get_all_students())

    # 3) UPDATE
    if new_id:
        print("\n=== UPDATE ===")
        updated = update_student_email(new_id, "alice.updated@example.com")
        print(f"Updated={updated}")
        print("\n=== AFTER UPDATE ===")
        print_students(get_all_students())

    # 4) DELETE
    if new_id:
        print("\n=== DELETE ===")
        deleted = delete_student(new_id)
        print(f"Deleted={deleted}")
        print("\n=== AFTER DELETE ===")
        print_students(get_all_students())

    # 5) (Optional) Constraint demo: duplicate email
    # print("\n=== DUPLICATE EMAIL TEST ===")
    # _ = add_student("John", "Doe", "john.doe@example.com", "2023-09-04")  # should trigger UNIQUE warning
    # print_students(get_all_students())


if __name__ == "__main__":
    demo_sequence()
