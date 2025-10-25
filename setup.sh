#!/bin/bash
# SixtyPercent Setup Script for Manjaro Linux

echo "=========================================="
echo "SixtyPercent Attendance Tracker - Setup"
echo "=========================================="
echo ""

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "⚠️  This script is designed for Linux systems"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Run: sudo pacman -S python python-pip"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if MySQL/MariaDB is installed
if ! command -v mysql &> /dev/null; then
    echo "❌ MySQL/MariaDB is not installed!"
    echo "Run: sudo pacman -S mariadb"
    echo "Then: sudo mariadb-install-db --user=mysql --basedir=/usr --datadir=/var/lib/mysql"
    echo "And: sudo systemctl start mariadb"
    exit 1
fi

echo "✅ MySQL/MariaDB found"

# Check if MySQL is running
if ! systemctl is-active --quiet mariadb && ! systemctl is-active --quiet mysql; then
    echo "⚠️  MySQL/MariaDB is not running"
    echo "Starting MariaDB..."
    sudo systemctl start mariadb
    if [ $? -eq 0 ]; then
        echo "✅ MariaDB started successfully"
    else
        echo "❌ Failed to start MariaDB. Please start it manually: sudo systemctl start mariadb"
        exit 1
    fi
else
    echo "✅ MySQL/MariaDB is running"
fi

# Create virtual environment
echo ""
echo "📦 Creating Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📥 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "🔐 Setting up environment variables..."
    cp .env.example .env
    echo "✅ Created .env file from template"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file with your MySQL credentials!"
    echo "   Run: nano .env"
else
    echo ""
    echo "✅ .env file already exists"
fi

# Database setup
echo ""
echo "🗄️  Database Setup"
echo "=================="
read -p "Do you want to set up the database now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Please enter your MySQL root password when prompted..."
    echo ""
    read -p "MySQL username (default: root): " DB_USER
    DB_USER=${DB_USER:-root}
    
    echo "Importing database schema..."
    mysql -u "$DB_USER" -p < schema.sql
    
    if [ $? -eq 0 ]; then
        echo "✅ Database created and populated successfully!"
        echo ""
        echo "🎉 Setup Complete!"
        echo ""
        echo "To start the application:"
        echo "  1. Edit .env file: nano .env"
        echo "  2. Activate venv: source venv/bin/activate"
        echo "  3. Run app: python app.py"
        echo "  4. Open browser: http://localhost:5000"
        echo ""
        echo "Demo Account:"
        echo "  Username: demo_student"
        echo "  Password: password123"
    else
        echo "❌ Database setup failed. Please check your MySQL credentials."
        echo "You can manually import the schema:"
        echo "  mysql -u root -p < schema.sql"
    fi
else
    echo ""
    echo "⚠️  Database not set up. To set up manually:"
    echo "   mysql -u root -p < schema.sql"
fi

echo ""
echo "=========================================="
echo "Setup process finished!"
echo "=========================================="
