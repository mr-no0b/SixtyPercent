#!/bin/bash
# Database Setup Fix for MariaDB on Manjaro

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     SixtyPercent - Database Setup Fix for MariaDB          ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

echo "This script will help fix the MariaDB authentication issue."
echo ""

echo "📋 Option 1: Use sudo to import (RECOMMENDED)"
echo "════════════════════════════════════════════════════════════════"
echo "This is the easiest method for MariaDB on Manjaro/Arch."
echo ""
read -p "Press Enter to import database with sudo..."
echo ""

sudo mariadb < schema.sql

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Database created successfully!"
    echo ""
    echo "Now update your .env file:"
    echo "  1. Open .env: nano .env"
    echo "  2. Keep DB_USER=root"
    echo "  3. Leave DB_PASSWORD empty (or set to your root password if you have one)"
    echo ""
    echo "Then run: ./start.sh"
    exit 0
else
    echo ""
    echo "❌ Import failed with sudo. Let's try alternative methods..."
    echo ""
fi

echo ""
echo "📋 Option 2: Create a dedicated database user"
echo "════════════════════════════════════════════════════════════════"
read -p "Do you want to create a dedicated user? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Creating database user 'attendance_user' with password 'attendance123'..."
    echo ""
    
    sudo mariadb << EOF
CREATE DATABASE IF NOT EXISTS sixtypercent CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'attendance_user'@'localhost' IDENTIFIED BY 'attendance123';
GRANT ALL PRIVILEGES ON sixtypercent.* TO 'attendance_user'@'localhost';
FLUSH PRIVILEGES;
EOF

    if [ $? -eq 0 ]; then
        echo "✅ User created successfully!"
        echo ""
        echo "Now importing schema..."
        mariadb -u attendance_user -pattendance123 sixtypercent < schema.sql
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "✅ Database setup complete!"
            echo ""
            echo "Update your .env file with these credentials:"
            echo "  DB_USER=attendance_user"
            echo "  DB_PASSWORD=attendance123"
            echo ""
            echo "Run: nano .env (to edit)"
            echo "Then: ./start.sh (to start app)"
            exit 0
        fi
    fi
fi

echo ""
echo "📋 Option 3: Manual Steps"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "If the above didn't work, follow these manual steps:"
echo ""
echo "1. Import database with sudo:"
echo "   sudo mariadb < schema.sql"
echo ""
echo "2. Create your .env file:"
echo "   cp .env.example .env"
echo ""
echo "3. Edit .env and use these settings:"
echo "   DB_HOST=localhost"
echo "   DB_USER=root"
echo "   DB_PASSWORD="
echo "   (leave password empty for socket auth)"
echo ""
echo "4. OR create a user in MariaDB:"
echo "   sudo mariadb"
echo "   Then run:"
echo "   CREATE USER 'myuser'@'localhost' IDENTIFIED BY 'mypassword';"
echo "   GRANT ALL PRIVILEGES ON sixtypercent.* TO 'myuser'@'localhost';"
echo "   FLUSH PRIVILEGES;"
echo "   EXIT;"
echo ""
echo "5. Import with your user:"
echo "   mariadb -u myuser -p sixtypercent < schema.sql"
echo ""
echo "6. Update .env with your credentials"
echo ""
echo "7. Start the app:"
echo "   ./start.sh"
echo ""
