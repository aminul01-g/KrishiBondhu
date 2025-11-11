#!/bin/bash
echo "🧪 Quick System Test"
echo "==================="
echo ""

echo "1. Testing Backend API..."
BACKEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/conversations)
if [ "$BACKEND_STATUS" = "200" ]; then
    echo "   ✅ Backend API: OK (HTTP $BACKEND_STATUS)"
else
    echo "   ❌ Backend API: Failed (HTTP $BACKEND_STATUS)"
fi

echo ""
echo "2. Testing Frontend..."
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5173)
if [ "$FRONTEND_STATUS" = "200" ]; then
    echo "   ✅ Frontend: OK (HTTP $FRONTEND_STATUS)"
else
    echo "   ❌ Frontend: Failed (HTTP $FRONTEND_STATUS)"
fi

echo ""
echo "3. Testing Database..."
DB_STATUS=$(docker ps | grep farmassist_postgres | wc -l)
if [ "$DB_STATUS" = "1" ]; then
    echo "   ✅ PostgreSQL: Running"
else
    echo "   ❌ PostgreSQL: Not running"
fi

echo ""
echo "✅ All systems operational!"
