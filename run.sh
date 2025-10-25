#!/bin/bash

# Run Website Script for SixtyPercent Attendance Tracker
# This script starts the Flask development server

echo "=========================================="
echo "  SixtyPercent Attendance Tracker"
echo "=========================================="
echo ""

# Check and start MariaDB/MySQL service
echo "🔧 Checking database server status..."
if sudo systemctl is-active --quiet mariadb; then
    echo "✅ MariaDB is already running"
elif sudo systemctl is-active --quiet mysql; then
    echo "✅ MySQL is already running"
else
    echo "⚠️  Database server is not running"
    echo "🚀 Starting MariaDB service..."
    
    # Try to start MariaDB first, then MySQL
    if sudo systemctl start mariadb 2>/dev/null; then
        echo "✅ MariaDB started successfully"
    elif sudo systemctl start mysql 2>/dev/null; then
        echo "✅ MySQL started successfully"
    else
        echo "❌ Error: Failed to start database server!"
        echo "   Please start it manually:"
        echo "   sudo systemctl start mariadb"
        echo "   or"
        echo "   sudo systemctl start mysql"
        exit 1
    fi
    
    # Wait a moment for the service to fully start
    sleep 2
fi

echo ""
echo "🚀 Starting Flask development server..."
echo ""
echo "📍 Access the website at:"
echo "   - http://127.0.0.1:5000"
echo "   - http://localhost:5000"
echo ""
echo "⚙️  Configuration:"
echo "   - Debug mode: ON"
echo "   - Auto-reload: ENABLED"
echo "   - Host: 0.0.0.0 (all interfaces)"
echo "   - Port: 5000"
echo ""
echo "💡 Tips:"
echo "   - Press CTRL+C to stop the server"
echo "   - Changes to code will auto-reload"
echo "   - Check .env file for database settings"
echo ""
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "🐍 Activating virtual environment..."
    source venv/bin/activate
fi

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "⚠️  Flask not found. Installing dependencies..."
    pip install flask flask-mysqldb python-dotenv
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "   Creating default .env file..."
    cat > .env << 'EOF'
MYSQL_HOST=localhost
MYSQL_USER=attendance_user
MYSQL_PASSWORD=attendance_password
MYSQL_DB=sixtypercent
SECRET_KEY=your-secret-key-change-this-in-production
EOF
    echo "✅ Created .env file. Please update with your settings."
fi

# Check if database is accessible
echo "🔍 Checking database connection..."
if sudo mariadb sixtypercent -e "SELECT 1;" > /dev/null 2>&1; then
    echo "✅ Database connection successful!"
else
    echo "❌ Error: Cannot connect to database!"
    echo "   Please check:"
    echo "   - MariaDB/MySQL is running"
    echo "   - Database 'sixtypercent' exists"
    echo "   - User credentials in .env are correct"
    echo ""
    read -p "Continue anyway? (yes/no): " continue
    if [ "$continue" != "yes" ]; then
        exit 1
    fi
fi

echo ""
echo "🌐 Starting server..."
echo ""

# Run Flask app
python3 app.py

# This line will execute when server stops
echo ""
echo "👋 Server stopped. Goodbye!"
