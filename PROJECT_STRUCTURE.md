# SixtyPercent Project Structure

```
Database/
│
├── 📄 app.py                    # Main Flask application (272 lines)
│                                 # - Routes for login, register, dashboard
│                                 # - Attendance marking and editing
│                                 # - Course enrollment management
│                                 # - Settings configuration
│
├── ⚙️  config.py                # Configuration settings
│                                 # - Database connection parameters
│                                 # - Loads from .env file
│
├── 🗄️  schema.sql               # MySQL database schema (168 lines)
│                                 # - Creates 6 tables + 1 view
│                                 # - Includes sample data
│                                 # Tables:
│                                 #   1. users (students)
│                                 #   2. teachers
│                                 #   3. courses
│                                 #   4. enrollments
│                                 #   5. attendance_records
│                                 #   6. attendance_settings
│
├── 📦 requirements.txt          # Python dependencies
│                                 # - Flask, Flask-MySQLdb, python-dotenv
│
├── 🔐 .env.example             # Environment template
├── 🔐 .env                     # Your config (create from .env.example)
│
├── 🚀 setup.sh                 # Automated setup script
├── ▶️  start.sh                 # Quick start script
│
├── 📖 README.md                # Complete documentation (285 lines)
├── ⚡ QUICKSTART.md            # Quick start guide
├── 🚫 .gitignore               # Git ignore rules
│
├── 📁 templates/               # HTML templates (7 files)
│   ├── base.html              # Base layout with navbar
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── dashboard.html         # Main dashboard
│   ├── course_detail.html     # Course details & attendance
│   ├── mark_attendance.html   # Mark attendance form
│   └── courses.html           # Browse/enroll courses
│
└── 📁 static/                  # Static files
    └── style.css              # CSS styling (700+ lines)
                               # - Responsive design
                               # - Purple gradient theme
                               # - Mobile-friendly

```

## Database Schema Diagram

```
┌─────────────┐
│   users     │
│─────────────│
│ id (PK)     │◄─────┐
│ username    │      │
│ password    │      │
│ full_name   │      │
│ email       │      │
└─────────────┘      │
                     │
                     │
┌─────────────┐      │         ┌──────────────────┐
│  teachers   │      │         │   enrollments    │
│─────────────│      │         │──────────────────│
│ id (PK)     │◄─┐   └─────────┤ user_id (FK)     │
│ name        │  │             │ course_id (FK)   │◄─────┐
│ email       │  │             │ id (PK)          │      │
│ department  │  │             └──────────────────┘      │
└─────────────┘  │                      ▲                │
                 │                      │                │
                 │                      │                │
┌─────────────┐  │                      │                │
│   courses   │  │                      │                │
│─────────────│  │                      │                │
│ id (PK)     │──┘   ┌──────────────────┴──────┐        │
│ course_code │      │  attendance_records     │        │
│ course_name │      │─────────────────────────│        │
│ teacher_id  │◄─┐   │ id (PK)                 │        │
│ semester    │  │   │ enrollment_id (FK)      │────────┘
│ total_class │  │   │ class_date              │
└─────────────┘  │   │ status (present/absent) │
                 │   │ notes                   │
                 │   └─────────────────────────┘
                 │
                 │   ┌─────────────────────────┐
                 │   │  attendance_settings    │
                 │   │─────────────────────────│
                 └───┤ user_id (FK)            │
                     │ course_id (FK)          │
                     │ required_percentage     │
                     └─────────────────────────┘
```

## Key Features by File

### app.py (Main Application)
- ✅ User authentication (login/register/logout)
- ✅ Dashboard with attendance overview
- ✅ Mark, edit, and delete attendance
- ✅ Course enrollment/unenrollment
- ✅ Customizable attendance percentage
- ✅ Real-time statistics calculation

### schema.sql (Database)
- ✅ 6 normalized tables with foreign keys
- ✅ Indexes for performance
- ✅ Sample data for testing
- ✅ View for attendance summary
- ✅ Constraints and data validation

### templates/ (Frontend)
- ✅ Responsive design
- ✅ Flash messages for feedback
- ✅ Forms with validation
- ✅ Color-coded attendance status
- ✅ Warning badges for low attendance

### style.css (Styling)
- ✅ Modern purple gradient theme
- ✅ Card-based layout
- ✅ Mobile responsive (media queries)
- ✅ Smooth animations and transitions
- ✅ Accessible color contrast

## Technology Stack

- **Backend:** Flask 3.0 (Python)
- **Database:** MySQL/MariaDB
- **Frontend:** HTML5, CSS3
- **Template Engine:** Jinja2
- **Security:** Werkzeug password hashing
- **Session Management:** Flask sessions

## Code Statistics

- **Total Python Code:** ~270 lines (app.py)
- **Total SQL:** ~170 lines (schema.sql)
- **Total HTML:** ~500 lines (all templates)
- **Total CSS:** ~700 lines (style.css)
- **Total Documentation:** ~400 lines (README + guides)
