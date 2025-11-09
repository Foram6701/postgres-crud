-- Create
INSERT INTO students (first_name, last_name, email, enrollment_date)
VALUES ('Alice', 'Brown', 'alice.brown@example.com', '2023-09-03');

-- Read
SELECT * FROM students ORDER BY student_id;

-- Update
UPDATE students
SET email = 'alice.updated@example.com'
WHERE student_id = 4;

-- Delete
DELETE FROM students
WHERE student_id = 4;
