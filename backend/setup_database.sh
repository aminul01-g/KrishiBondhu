#!/bin/bash
# Database setup and migration script

set -e

echo "🗄️  FarmerAI Database Setup"
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found"
    echo "   Please create .env file with DATABASE_URL"
    exit 1
fi

# Load environment variables
source .env 2>/dev/null || true

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "❌ Virtual environment not found"
    exit 1
fi

# Check if PostgreSQL is running
echo "🔍 Checking PostgreSQL connection..."
if command -v pg_isready &> /dev/null; then
    if pg_isready -h localhost -p 5432 &> /dev/null; then
        echo "✅ PostgreSQL is running"
    else
        echo "⚠️  PostgreSQL is not running"
        echo "   Starting with Docker Compose..."
        docker-compose up -d postgres
        echo "   Waiting for PostgreSQL to be ready..."
        sleep 5
    fi
else
    echo "⚠️  pg_isready not found, assuming PostgreSQL is running via Docker"
fi

# Run migrations
echo ""
echo "🔄 Running database migrations..."
alembic upgrade head

if [ $? -eq 0 ]; then
    echo "✅ Database migrations completed successfully"
else
    echo "❌ Database migrations failed"
    echo "   Make sure PostgreSQL is running and DATABASE_URL is correct in .env"
    exit 1
fi

# Verify tables
echo ""
echo "🔍 Verifying database tables..."
python3 << EOF
import asyncio
from app.db import AsyncSessionLocal, engine
from app.models.db_models import Base, User, Conversation
from sqlalchemy import inspect

async def verify_tables():
    async with AsyncSessionLocal() as session:
        # Check if tables exist
        inspector = inspect(engine.sync_engine)
        tables = inspector.get_table_names()
        
        if 'users' in tables and 'conversations' in tables:
            print("✅ Tables created successfully")
            print(f"   Tables: {', '.join(tables)}")
        else:
            print("❌ Tables not found")
            print(f"   Found tables: {', '.join(tables)}")

asyncio.run(verify_tables())
EOF

echo ""
echo "✅ Database setup completed!"

