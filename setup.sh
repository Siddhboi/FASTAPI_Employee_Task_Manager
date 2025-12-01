#!/bin/bash

# Employee Task Manager API - Setup Script
# This script sets up the development environment

echo "🚀 Employee Task Manager API - Setup"
echo "======================================"

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created. Please update it with your settings."
else
    echo "✅ .env file already exists"
fi

# Initialize Alembic migrations
echo ""
echo "🗄️  Setting up database migrations..."
if [ ! -d "alembic/versions" ]; then
    mkdir -p alembic/versions
    echo "✅ Alembic versions directory created"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Update .env file with your configuration"
echo "3. Run migrations: alembic revision --autogenerate -m 'Initial migration'"
echo "4. Apply migrations: alembic upgrade head"
echo "5. Populate sample data: python sample_data.py"
echo "6. Populate default_user: python create_default_users.py"
echo "6. Start the server: uvicorn main:app --reload"
echo ""
echo "🎉 Happy coding!"