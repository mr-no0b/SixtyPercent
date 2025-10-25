# 🔧 FIXED: MariaDB Authentication Issue on Manjaro

## Problem
```
MySQLdb.OperationalError: (1698, "Access denied for user 'root'@'localhost'")
```

## Root Cause
MariaDB on Manjaro/Arch Linux uses Unix socket authentication by default for the root user, which doesn't work well with Flask-MySQLdb.

## ✅ Solution Applied

### 1. Created a dedicated MySQL user with password authentication
```bash
sudo mariadb -e "CREATE USER IF NOT EXISTS 'attendance_user'@'localhost' IDENTIFIED BY 'attendance123';"
sudo mariadb -e "GRANT ALL PRIVILEGES ON sixtypercent.* TO 'attendance_user'@'localhost';"
sudo mariadb -e "FLUSH PRIVILEGES;"
```

### 2. Updated .env file
```env
DB_HOST=localhost
DB_USER=attendance_user
DB_PASSWORD=attendance123
DB_NAME=sixtypercent
```

### 3. Restarted Flask application
```bash
source venv/bin/activate
python app.py
```

## ✅ Current Status

**Database User:** `attendance_user`  
**Password:** `attendance123`  
**Database:** `sixtypercent`  
**Status:** ✅ Working!

## 🌐 Access the Application

Open your browser: **http://localhost:5000**

**Demo Account:**
- Username: `demo_student`
- Password: `password123`

## 🔒 Security Note

For personal use, the current setup is fine. If you deploy this to production:

1. Change the database password to something stronger
2. Update SECRET_KEY in .env
3. Set FLASK_ENV=production
4. Use a proper WSGI server (gunicorn/uWSGI)
5. Enable HTTPS

## 🎯 Alternative Solutions

If you prefer to use root (not recommended):

**Option 1: Set root password**
```bash
sudo mariadb
ALTER USER 'root'@'localhost' IDENTIFIED BY 'your_password';
FLUSH PRIVILEGES;
```
Then update .env:
```env
DB_USER=root
DB_PASSWORD=your_password
```

**Option 2: Change root to password auth (instead of unix_socket)**
```bash
sudo mariadb
ALTER USER 'root'@'localhost' IDENTIFIED VIA mysql_native_password USING PASSWORD('your_password');
FLUSH PRIVILEGES;
```

## 📝 Testing Database Connection

Test the connection manually:
```bash
mariadb -u attendance_user -pattendance123 sixtypercent -e "SELECT COUNT(*) FROM users;"
```

Should show: `1` (the demo user)

## 🎉 Everything Working Now!

The application should now be fully functional with:
- ✅ Working database connection
- ✅ User authentication
- ✅ All 6 tables accessible
- ✅ Demo data available

Happy tracking! 📚✨
