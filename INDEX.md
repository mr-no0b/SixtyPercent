# 📚 SixtyPercent - Complete Project Index

## 🎯 Project Overview
**Name:** SixtyPercent  
**Type:** Flask Web Application  
**Purpose:** Personal attendance tracking for university students  
**Database:** MySQL (6 tables)  
**Theme:** Purple gradient, simple and clean design  

---

## 📁 Complete File List (21 files)

### 🔧 Core Application Files (4)
1. **app.py** (272 lines)
   - Main Flask application
   - All routes and business logic
   - Authentication, attendance tracking, course management

2. **config.py** (18 lines)
   - Configuration loader
   - Database connection settings
   - Reads from .env file

3. **requirements.txt** (4 packages)
   - Flask==3.0.0
   - Flask-MySQLdb==2.0.0
   - python-dotenv==1.0.0
   - werkzeug==3.0.1

4. **schema.sql** (168 lines)
   - Complete database schema
   - 6 tables + 1 view
   - Sample data included

### 🎨 Frontend Files (8)
**Templates Directory (7 HTML files):**
- base.html - Base layout with navigation
- login.html - User login page
- register.html - Registration form
- dashboard.html - Main dashboard with course cards
- course_detail.html - Course details and attendance table
- mark_attendance.html - Mark attendance form
- courses.html - Browse and enroll in courses

**Static Directory (1 CSS file):**
- style.css (700+ lines) - Complete responsive styling

### 📖 Documentation Files (5)
1. **README.md** (285 lines)
   - Complete setup guide for Manjaro
   - Installation instructions
   - Troubleshooting guide
   - Usage documentation

2. **QUICKSTART.md** (72 lines)
   - Quick start guide
   - Essential commands
   - Demo account info

3. **SUMMARY.md** (192 lines)
   - Project completion summary
   - Feature checklist
   - Technology stack
   - Next steps

4. **PROJECT_STRUCTURE.md** (190 lines)
   - Visual project structure
   - Database schema diagram
   - Code statistics

5. **ARCHITECTURE.txt** (156 lines)
   - System architecture diagram
   - Data flow visualization
   - Component relationships

### ⚙️ Configuration Files (2)
1. **.env.example** (7 lines)
   - Environment variables template
   - Database credentials format

2. **.gitignore** (17 lines)
   - Git ignore rules
   - Protects sensitive files

### 🚀 Utility Scripts (2)
1. **setup.sh** (95 lines)
   - Automated setup script
   - Checks prerequisites
   - Creates venv and installs packages
   - Sets up database

2. **start.sh** (22 lines)
   - Quick start script
   - Activates venv
   - Runs Flask application

---

## 📊 Statistics

### Code Metrics
- **Total Python:** ~290 lines
- **Total SQL:** ~170 lines  
- **Total HTML:** ~500 lines
- **Total CSS:** ~700 lines
- **Total Documentation:** ~900 lines
- **Total Scripts:** ~120 lines

### Project Totals
- **21 Total Files**
- **6 Database Tables**
- **7 HTML Templates**
- **10+ Routes**
- **~2,700 Total Lines**

---

## 🗄️ Database Tables

1. **users** - Student accounts (id, username, password, name, email)
2. **teachers** - Teacher info (id, name, email, department)
3. **courses** - Course details (id, code, name, teacher, semester)
4. **enrollments** - Student enrollments (id, user_id, course_id)
5. **attendance_records** - Attendance entries (id, enrollment_id, date, status)
6. **attendance_settings** - Custom percentages (id, user_id, course_id, %)

**Plus 1 View:** attendance_summary (joins all tables for dashboard)

---

## 🎨 Pages & Routes

### Public Routes
- `GET /` - Redirects to login or dashboard
- `GET/POST /login` - User authentication
- `GET/POST /register` - User registration

### Protected Routes (Login Required)
- `GET /dashboard` - Main dashboard
- `GET /courses` - Browse all courses
- `GET /course/<id>` - Course details
- `GET/POST /course/<id>/mark` - Mark attendance
- `POST /course/<id>/enroll` - Enroll in course
- `POST /course/<id>/unenroll` - Unenroll from course
- `POST /course/<id>/settings` - Update percentage
- `POST /attendance/<id>/edit` - Edit attendance
- `POST /attendance/<id>/delete` - Delete record
- `GET /logout` - Logout

---

## 🎯 Key Features Implemented

### ✅ Authentication & Security
- User registration with password hashing
- Secure login system
- Session management
- Protected routes

### ✅ Attendance Management
- Mark daily attendance (present/absent)
- Edit existing records
- Delete records
- Add notes to each entry

### ✅ Course Management
- Browse available courses
- Enroll/unenroll functionality
- View course details
- Teacher information

### ✅ Statistics & Analytics
- Real-time percentage calculation
- Present/absent counts
- Visual dashboard with cards
- Warning badges for low attendance

### ✅ Customization
- Editable attendance percentage (default 60%)
- Per-course settings
- Flexible threshold (0-100%)

### ✅ User Interface
- Responsive design (mobile + desktop)
- Modern purple gradient theme
- Card-based layout
- Flash messages
- Form validation

---

## 🚀 Quick Start

```bash
# 1. Setup (run once)
./setup.sh

# 2. Configure
nano .env

# 3. Start server
./start.sh

# 4. Open browser
http://localhost:5000

# Demo login:
# Username: demo_student
# Password: password123
```

---

## 📖 Documentation Hierarchy

```
START HERE → QUICKSTART.md
             ↓
Full Guide → README.md
             ↓
Structure  → PROJECT_STRUCTURE.md
             ↓
Summary    → SUMMARY.md
             ↓
Technical  → ARCHITECTURE.txt
```

---

## 🛠️ Technology Stack

- **Backend:** Flask 3.0 (Python)
- **Database:** MySQL/MariaDB
- **Frontend:** HTML5 + CSS3
- **Template:** Jinja2
- **Auth:** Werkzeug (pbkdf2:sha256)
- **Connector:** Flask-MySQLdb
- **Config:** python-dotenv

---

## 📝 Sample Data Included

- ✅ 1 demo student account
- ✅ 4 teachers
- ✅ 5 courses (CS, Math, Physics)
- ✅ Sample enrollments
- ✅ ~35 attendance records

---

## 🎨 Design Highlights

- **Colors:** Purple gradient (#667eea to #764ba2)
- **Cards:** White with shadows and hover effects
- **Status:** Green for good, red for bad
- **Layout:** Responsive grid system
- **Typography:** Segoe UI font family
- **Animations:** Smooth transitions (0.3s)

---

## 🔒 Security Features

- ✅ Password hashing (Werkzeug)
- ✅ Session-based auth
- ✅ SQL injection prevention (parameterized queries)
- ✅ Login required decorators
- ✅ Environment variable protection
- ✅ .gitignore for sensitive files

---

## 📦 Dependencies

```
Flask==3.0.0           # Web framework
Flask-MySQLdb==2.0.0   # MySQL connector
python-dotenv==1.0.0   # Environment variables
werkzeug==3.0.1        # Security utilities
```

---

## ✨ What Makes This Project Special

1. **Complete** - Fully functional, no placeholders
2. **Simple** - Clean code, easy to understand
3. **Documented** - Extensive documentation
4. **Tested** - Includes sample data
5. **Automated** - Setup scripts included
6. **Responsive** - Works on all devices
7. **Customizable** - Adjustable percentages
8. **Secure** - Password hashing, protected routes
9. **Database-Driven** - Proper MySQL schema with 6 tables
10. **Production-Ready** - With minor modifications

---

## 🎓 Perfect For

- University students tracking attendance
- Personal attendance management
- Learning Flask and MySQL
- Portfolio projects
- Real-world application example

---

## 📞 Need Help?

1. **Quick Help:** Check QUICKSTART.md
2. **Full Guide:** Read README.md
3. **Structure:** See PROJECT_STRUCTURE.md
4. **Troubleshooting:** README.md has solutions
5. **Architecture:** Review ARCHITECTURE.txt

---

## 🎉 Project Status: COMPLETE ✅

All requirements met:
✅ Flask application
✅ MySQL database with 6+ tables
✅ Authentication system
✅ Attendance tracking
✅ Customizable 60% threshold
✅ Simple and clean design
✅ Full documentation
✅ Ready to run on Manjaro

---

**Made with ❤️ for students who need to track that crucial 60% attendance!**

*Happy tracking! 📚✨*
