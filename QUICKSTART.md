# 🚀 QUICK START GUIDE

## For First Time Setup (Run Once)

```bash
# 1. Make sure MariaDB/MySQL is installed and running
sudo pacman -S mariadb
sudo systemctl start mariadb

# 2. Run the automated setup script
./setup.sh

# 3. Edit environment variables with your MySQL password
nano .env

# 4. Start the application
./start.sh
```

## For Regular Use (After Setup)

```bash
# Simply run:
./start.sh

# Or manually:
source venv/bin/activate
python app.py
```

## Access the Website

Open your browser and go to: **http://localhost:5000**

## Demo Login

- **Username:** demo_student
- **Password:** password123

## Common Commands

### View project structure:
```bash
tree -L 2 -I 'venv|__pycache__'
```

### Check MySQL database:
```bash
mysql -u root -p
USE sixtypercent;
SHOW TABLES;
```

### Reset database (⚠️ deletes all data):
```bash
mysql -u root -p < schema.sql
```

### Stop the server:
Press `Ctrl+C` in the terminal

## What You Can Do

1. ✅ **Dashboard** - View all your courses and attendance percentages
2. 📚 **Enroll** - Browse and enroll in available courses
3. 📝 **Mark Attendance** - Record your daily attendance (present/absent)
4. ⚙️ **Settings** - Change required percentage per course (default 60%)
5. 📊 **Statistics** - Automatic calculation of attendance stats
6. ✏️ **Edit** - Modify or delete attendance records

## Project Features

- **6 MySQL Tables:** users, teachers, courses, enrollments, attendance_records, attendance_settings
- **Authentication:** Secure login/register system
- **Responsive:** Works on desktop and mobile
- **Simple:** Clean, intuitive interface
- **Customizable:** Set your own attendance targets

## Need Help?

Check the full README.md for detailed documentation!
