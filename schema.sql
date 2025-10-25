-- SixtyPercent Attendance Tracker Database Schema
-- Drop existing database and create fresh
DROP DATABASE IF EXISTS sixtypercent;
CREATE DATABASE sixtypercent CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE sixtypercent;

-- Table 1: Users (Students)
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (username)
) ENGINE=InnoDB;

-- Table 2: Teachers
CREATE TABLE teachers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    department VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_name (name),
    INDEX idx_user (user_id)
) ENGINE=InnoDB;

-- Table 3: Courses
CREATE TABLE courses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    course_code VARCHAR(20) NOT NULL,
    course_name VARCHAR(150) NOT NULL,
    teacher_id INT NOT NULL,
    semester VARCHAR(20),
    total_classes INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_course (user_id, course_code),
    INDEX idx_course_code (course_code),
    INDEX idx_teacher (teacher_id),
    INDEX idx_user (user_id)
) ENGINE=InnoDB;

-- Table 4: Student Course Enrollment
CREATE TABLE enrollments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    course_id INT NOT NULL,
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    UNIQUE KEY unique_enrollment (user_id, course_id),
    INDEX idx_user (user_id),
    INDEX idx_course (course_id)
) ENGINE=InnoDB;

-- Table 5: Attendance Records
CREATE TABLE attendance_records (
    id INT PRIMARY KEY AUTO_INCREMENT,
    enrollment_id INT NOT NULL,
    class_date DATE NOT NULL,
    status ENUM('present', 'absent') NOT NULL,
    notes VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (enrollment_id) REFERENCES enrollments(id) ON DELETE CASCADE,
    UNIQUE KEY unique_attendance (enrollment_id, class_date),
    INDEX idx_enrollment (enrollment_id),
    INDEX idx_date (class_date)
) ENGINE=InnoDB;

-- Table 6: Attendance Settings (for customizable percentage threshold)
CREATE TABLE attendance_settings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    course_id INT NOT NULL,
    required_percentage DECIMAL(5,2) DEFAULT 60.00,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    UNIQUE KEY unique_setting (user_id, course_id),
    INDEX idx_user_course (user_id, course_id)
) ENGINE=InnoDB;

-- No sample data - users will create their own courses and teachers!

-- Create a view for easy attendance summary
CREATE VIEW attendance_summary AS
SELECT 
    u.id as user_id,
    u.full_name,
    c.id as course_id,
    c.course_code,
    c.course_name,
    t.name as teacher_name,
    COUNT(ar.id) as total_marked,
    SUM(CASE WHEN ar.status = 'present' THEN 1 ELSE 0 END) as present_count,
    SUM(CASE WHEN ar.status = 'absent' THEN 1 ELSE 0 END) as absent_count,
    ROUND((SUM(CASE WHEN ar.status = 'present' THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(ar.id), 0)), 2) as attendance_percentage,
    COALESCE(ats.required_percentage, 60.00) as required_percentage
FROM users u
JOIN enrollments e ON u.id = e.user_id
JOIN courses c ON e.course_id = c.id
JOIN teachers t ON c.teacher_id = t.id
LEFT JOIN attendance_records ar ON e.id = ar.enrollment_id
LEFT JOIN attendance_settings ats ON u.id = ats.user_id AND c.id = ats.course_id
GROUP BY u.id, c.id, u.full_name, c.course_code, c.course_name, t.name, ats.required_percentage;
