#!/bin/bash
# Start script for FarmerAI backend server

set -e

echo "🚀 Starting FarmerAI Backend Server..."
echo ""

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "❌ Virtual environment not found. Please run: python3 -m venv venv"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Creating from template..."
    echo "GEMINI_API_KEY=AIzaSyDlWQCKSKKtHl1wLQvnb9QaPRUODn8sMQ0" > .env
    echo "DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/farmdb" >> .env
    echo "UPLOAD_DIR=/tmp/uploads" >> .env
    echo "✅ Created .env file"
fi

# Create upload directory
mkdir -p /tmp/uploads
echo "✅ Upload directory ready: /tmp/uploads"

# Check if PostgreSQL is running (optional)
if command -v pg_isready &> /dev/null; then
    if pg_isready -h localhost -p 5432 &> /dev/null; then
        echo "✅ PostgreSQL is running"
    else
        echo "⚠️  Warning: PostgreSQL is not running. Database features will not work."
        echo "   Start PostgreSQL with: docker-compose up -d postgres"
    fi
else
    echo "⚠️  Warning: PostgreSQL not found. Database features will not work."
fi

# Start the server
echo ""
echo "🌐 Starting FastAPI server on http://localhost:8000"
echo "📚 API docs available at http://localhost:8000/docs"
echo ""

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

