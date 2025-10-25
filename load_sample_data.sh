#!/bin/bash

# Sample Data Script for SixtyPercent Attendance Tracker
# This script populates the database with sample data for testing

echo "=========================================="
echo "  SixtyPercent - Load Sample Data"
echo "=========================================="
echo ""
echo "📦 Loading sample data into database..."
echo ""

sudo mariadb sixtypercent <<EOF
-- Delete existing demo user if exists
DELETE FROM users WHERE username = 'demo';

-- Insert sample user (username: demo, password: demo123)
INSERT INTO users (username, password_hash, full_name, email) VALUES
('demo', 'scrypt:32768:8:1\$pj7l8VLN2YLA4dc1\$58ca6b3c9143079a5499703fff0fbd98e5fc8aba238f7413a4b0b2424fe35abb0fba9386d4191ff7546c768991cf2b4cd9239641a43b7c2bb689138ab93925a1', 'Demo Student', 'demo@example.com');

SET @user_id = LAST_INSERT_ID();

-- Insert sample teachers
INSERT INTO teachers (user_id, name, department, email) VALUES
(@user_id, 'Dr. Sarah Johnson', 'Computer Science', 'sarah.johnson@university.edu'),
(@user_id, 'Prof. Michael Chen', 'Mathematics', 'michael.chen@university.edu'),
(@user_id, 'Dr. Emily Rodriguez', 'Physics', 'emily.rodriguez@university.edu'),
(@user_id, 'Prof. David Kumar', 'Chemistry', 'david.kumar@university.edu'),
(@user_id, 'Dr. Lisa Anderson', 'English', 'lisa.anderson@university.edu');

-- Insert sample courses
INSERT INTO courses (user_id, teacher_id, course_code, course_name, semester, total_classes) VALUES
(@user_id, 1, 'CS301', 'Database Systems', 'Fall 2025', 40),
(@user_id, 2, 'MATH201', 'Calculus II', 'Fall 2025', 45),
(@user_id, 3, 'PHY101', 'Physics I', 'Fall 2025', 50),
(@user_id, 4, 'CHEM102', 'Organic Chemistry', 'Fall 2025', 42),
(@user_id, 5, 'ENG201', 'English Literature', 'Fall 2025', 30);

-- Insert enrollments
INSERT INTO enrollments (user_id, course_id) VALUES
(@user_id, 1),
(@user_id, 2),
(@user_id, 3),
(@user_id, 4),
(@user_id, 5);

-- Insert attendance settings
INSERT INTO attendance_settings (user_id, course_id, required_percentage) VALUES
(@user_id, 1, 60.00),
(@user_id, 2, 75.00),
(@user_id, 3, 60.00),
(@user_id, 4, 70.00),
(@user_id, 5, 80.00);

-- Insert sample attendance records for CS301 (some present, some absent)
INSERT INTO attendance_records (enrollment_id, class_date, status, notes) VALUES
(1, '2025-10-01', 'present', 'Introduction to Databases'),
(1, '2025-10-03', 'present', 'ER Diagrams'),
(1, '2025-10-05', 'absent', 'Sick'),
(1, '2025-10-08', 'present', 'SQL Basics'),
(1, '2025-10-10', 'present', 'Normalization'),
(1, '2025-10-12', 'absent', 'Personal work'),
(1, '2025-10-15', 'present', 'Joins'),
(1, '2025-10-17', 'present', 'Transactions'),
(1, '2025-10-19', 'present', 'Indexes'),
(1, '2025-10-22', 'present', 'Query Optimization');

-- Insert sample attendance for MATH201 (mostly present)
INSERT INTO attendance_records (enrollment_id, class_date, status, notes) VALUES
(2, '2025-10-02', 'present', 'Integration techniques'),
(2, '2025-10-04', 'present', 'Substitution method'),
(2, '2025-10-06', 'present', 'Integration by parts'),
(2, '2025-10-09', 'present', 'Trigonometric integrals'),
(2, '2025-10-11', 'present', 'Partial fractions'),
(2, '2025-10-13', 'present', 'Applications'),
(2, '2025-10-16', 'present', 'Series'),
(2, '2025-10-18', 'absent', 'Family emergency');

-- Insert sample attendance for PHY101 (mixed)
INSERT INTO attendance_records (enrollment_id, class_date, status, notes) VALUES
(3, '2025-10-01', 'present', 'Kinematics'),
(3, '2025-10-03', 'present', 'Velocity and acceleration'),
(3, '2025-10-05', 'present', 'Newton laws'),
(3, '2025-10-08', 'absent', 'Sports event'),
(3, '2025-10-10', 'present', 'Forces'),
(3, '2025-10-12', 'absent', 'Unwell');

-- Insert sample attendance for CHEM102 (few records)
INSERT INTO attendance_records (enrollment_id, class_date, status, notes) VALUES
(4, '2025-10-02', 'present', 'Alkanes'),
(4, '2025-10-04', 'present', 'Alkenes'),
(4, '2025-10-06', 'absent', 'Lab conflict'),
(4, '2025-10-09', 'present', 'Alkynes');

-- Insert sample attendance for ENG201 (good attendance)
INSERT INTO attendance_records (enrollment_id, class_date, status, notes) VALUES
(5, '2025-10-01', 'present', 'Shakespeare introduction'),
(5, '2025-10-03', 'present', 'Romeo and Juliet'),
(5, '2025-10-05', 'present', 'Hamlet'),
(5, '2025-10-08', 'present', 'Macbeth'),
(5, '2025-10-10', 'present', 'Poetry analysis');

EOF

if [ $? -eq 0 ]; then
    echo "✅ Sample data loaded successfully!"
    echo ""
    echo "📊 Database Summary:"
    sudo mariadb sixtypercent -e "
    SELECT 
        (SELECT COUNT(*) FROM users) as users,
        (SELECT COUNT(*) FROM teachers) as teachers,
        (SELECT COUNT(*) FROM courses) as courses,
        (SELECT COUNT(*) FROM enrollments) as enrollments,
        (SELECT COUNT(*) FROM attendance_records) as attendance_records,
        (SELECT COUNT(*) FROM attendance_settings) as attendance_settings;
    "
    echo ""
    echo "👤 Demo Account:"
    echo "   Username: demo"
    echo "   Password: demo123"
    echo ""
    echo "   Note: You'll need to manually hash the password or register through the app."
    echo ""
    echo "🎓 Sample Courses:"
    echo "   - CS301: Database Systems (60% required, 10 classes marked)"
    echo "   - MATH201: Calculus II (75% required, 8 classes marked)"
    echo "   - PHY101: Physics I (60% required, 6 classes marked)"
    echo "   - CHEM102: Organic Chemistry (70% required, 4 classes marked)"
    echo "   - ENG201: English Literature (80% required, 5 classes marked)"
    echo ""
    echo "✨ Ready to use! Register a new account or use sample data."
else
    echo "❌ Error loading sample data!"
    exit 1
fi
