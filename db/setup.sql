INSERT INTO students (first_name, last_name, email, enrollment_date)
VALUES
('John', 'Doe', 'john.doe@example.com', '2023-09-01'),
('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02');

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
