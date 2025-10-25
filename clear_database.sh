#!/bin/bash

# Clear Database Script for SixtyPercent Attendance Tracker
# This script clears all data from the database while keeping the structure intact

echo "=========================================="
echo "  SixtyPercent - Clear Database"
echo "=========================================="
echo ""
echo "⚠️  WARNING: This will delete ALL data from the database!"
echo "   - All user accounts"
echo "   - All teachers"
echo "   - All courses"
echo "   - All attendance records"
echo ""
read -p "Are you sure you want to continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "❌ Operation cancelled."
    exit 0
fi

echo ""
echo "🗑️  Clearing database..."

sudo mariadb sixtypercent <<EOF
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE attendance_records;
TRUNCATE TABLE attendance_settings;
TRUNCATE TABLE enrollments;
TRUNCATE TABLE courses;
TRUNCATE TABLE teachers;
TRUNCATE TABLE users;
SET FOREIGN_KEY_CHECKS = 1;
EOF

if [ $? -eq 0 ]; then
    echo "✅ Database cleared successfully!"
    echo ""
    echo "📊 Verification:"
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
    echo "✨ Database is now empty and ready for fresh data!"
else
    echo "❌ Error clearing database!"
    exit 1
fi
