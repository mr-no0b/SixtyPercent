# SixtyPercent - Attendance Tracker

A Flask-based web application for tracking student attendance. The name comes from the typical university requirement of maintaining at least 60% attendance in each course, though this percentage is fully customizable per course.

## Features

- 📊 **Dashboard** - Visual overview of all enrolled courses and attendance percentages
- 📚 **Course Management** - Enroll/unenroll from courses, view course details
- ✅ **Attendance Tracking** - Mark daily attendance (present/absent) with notes
- 🎯 **Customizable Thresholds** - Set required attendance percentage per course (default 60%)
- 👨‍🏫 **Teacher & Course Info** - Track courses with teacher details
- 📈 **Real-time Statistics** - Automatic calculation of attendance percentages
- 🔐 **User Authentication** - Secure login and registration system

## Database Schema

The application uses 6 MySQL tables:

1. **users** - Student accounts
2. **teachers** - Teacher information
3. **courses** - Course details with teacher assignments
4. **enrollments** - Student-course enrollment mapping
5. **attendance_records** - Daily attendance entries
6. **attendance_settings** - Customizable percentage requirements per student/course

## Prerequisites (Manjaro Linux)

### 1. Install MySQL/MariaDB

```bash
# Install MariaDB (MySQL drop-in replacement)
sudo pacman -S mariadb

# Initialize the database
sudo mariadb-install-db --user=mysql --basedir=/usr --datadir=/var/lib/mysql

# Start MariaDB service
sudo systemctl start mariadb
sudo systemctl enable mariadb

# Secure your installation (set root password)
sudo mysql_secure_installation
```

### 2. Install Python and Development Tools

```bash
# Install Python 3 and pip
sudo pacman -S python python-pip

# Install MySQL client development files
sudo pacman -S mariadb-libs
```

### 3. Install Python Virtual Environment

```bash
# Install virtualenv
sudo pacman -S python-virtualenv
```

## Installation Steps

### 1. Clone/Navigate to Project Directory

```bash
cd /home/lionking/Documents/Database
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up MySQL Database

```bash
# Login to MySQL as root
mysql -u root -p

# Create database and user (optional - you can use root)
# Enter these commands in MySQL prompt:
```

```sql
CREATE DATABASE sixtypercent CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'attendance_user'@'localhost' IDENTIFIED BY 'your_password_here';
GRANT ALL PRIVILEGES ON sixtypercent.* TO 'attendance_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 5. Import Database Schema

```bash
# Import the schema.sql file
mysql -u root -p < schema.sql

# Or if you created a specific user:
mysql -u attendance_user -p < schema.sql
```

### 6. Configure Environment Variables

```bash
# Copy the example .env file
cp .env.example .env

# Edit the .env file with your database credentials
nano .env
```

Update the `.env` file:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=sixtypercent

SECRET_KEY=your-secret-key-change-this-to-random-string
FLASK_ENV=development
```

## Running the Application

### 1. Activate Virtual Environment (if not already activated)

```bash
source venv/bin/activate
```

### 2. Run the Flask Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### 3. Access the Website

Open your web browser and go to:
```
http://localhost:5000
```

## Default Demo Account

The database comes with a pre-populated demo account:

- **Username:** `demo_student`
- **Password:** `password123`

This account has sample courses and attendance data for testing.

## Creating Your Own Account

1. Click "Register here" on the login page
2. Fill in your details:
   - Full Name
   - Username
   - Email (optional)
   - Password
3. Click "Register"
4. Login with your new credentials

## Usage Guide

### Dashboard
- View all enrolled courses
- See attendance percentage at a glance
- Identify courses below required attendance (highlighted in yellow)

### Mark Attendance
1. Click "View Details" on any course card
2. Click "Mark Attendance" button
3. Select date, status (Present/Absent), and optional notes
4. Click "Save Attendance"

### Change Required Percentage
1. Go to course details page
2. Find "Attendance Settings" section
3. Enter new percentage (e.g., 75 for 75%)
4. Click "Update"

### Enroll in Courses
1. Go to "All Courses" from navigation
2. Browse available courses
3. Click "Enroll" on any course
4. Start marking attendance

### Edit Attendance
- From course details page, use dropdown to change status
- Click trash icon to delete a record

## Project Structure

```
Database/
├── app.py                  # Main Flask application
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── schema.sql             # MySQL database schema
├── .env.example           # Environment variables template
├── .env                   # Your environment variables (create this)
├── static/
│   └── style.css          # CSS styling
└── templates/
    ├── base.html          # Base template
    ├── login.html         # Login page
    ├── register.html      # Registration page
    ├── dashboard.html     # Main dashboard
    ├── course_detail.html # Course details
    ├── mark_attendance.html # Attendance form
    └── courses.html       # All courses list
```

## Troubleshooting

### MySQL Connection Issues

```bash
# Check if MySQL is running
sudo systemctl status mariadb

# Start MySQL if stopped
sudo systemctl start mariadb

# Check MySQL logs
sudo journalctl -u mariadb -n 50
```

### Python Package Issues

```bash
# Ensure you're in virtual environment
source venv/bin/activate

# Reinstall packages
pip install --upgrade -r requirements.txt
```

### Port Already in Use

If port 5000 is busy, edit `app.py` and change:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use different port
```

### Database Import Errors

```bash
# Check if database exists
mysql -u root -p -e "SHOW DATABASES;"

# Manually create database if needed
mysql -u root -p -e "CREATE DATABASE sixtypercent;"

# Then import schema
mysql -u root -p sixtypercent < schema.sql
```

## Security Notes

⚠️ **Important for Production:**

1. Change the `SECRET_KEY` in `.env` to a strong random string
2. Use a dedicated MySQL user (not root) with limited privileges
3. Set `FLASK_ENV=production` in `.env`
4. Use a proper WSGI server (gunicorn/uWSGI) instead of Flask development server
5. Enable HTTPS with SSL certificates
6. Keep your `.env` file secure and never commit it to git

## Adding Sample Data

The schema.sql already includes sample data:
- 4 teachers
- 5 courses
- 1 demo student account
- Sample enrollment and attendance records

To add more teachers/courses, use MySQL:

```sql
-- Add a new teacher
INSERT INTO teachers (name, email, department) 
VALUES ('Dr. Jane Doe', 'jane@university.edu', 'Computer Science');

-- Add a new course (use teacher_id from above)
INSERT INTO courses (course_code, course_name, teacher_id, semester, total_classes) 
VALUES ('CS401', 'Advanced Algorithms', 5, 'Fall 2025', 45);
```

## Stopping the Application

1. Press `Ctrl+C` in the terminal running Flask
2. Deactivate virtual environment:
```bash
deactivate
```

## License

This is a personal project for educational purposes.

## Support

For issues or questions, check:
- MySQL connection settings in `.env`
- Flask error messages in terminal
- Browser console for frontend errors

---

**Made with ❤️ for students who need to track that crucial 60% attendance!**
