#!/bin/bash

# Quick Docker Testing Script
# Run this to verify everything is working

echo "🐳 SequoAlpha Docker Test Suite"
echo "================================"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Start containers
echo "🚀 Starting containers..."
docker-compose up -d

# Wait for containers to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check container status
echo ""
echo "📊 Container Status:"
docker-compose ps

echo ""
echo "🧪 Running Tests..."
echo ""

# Test 1: Backend API
echo "Test 1: Backend API (http://localhost:8000)"
BACKEND_RESPONSE=$(curl -s http://localhost:8000/)
if echo "$BACKEND_RESPONSE" | grep -q "SequoAlpha"; then
    echo "✅ Backend is responding"
else
    echo "❌ Backend is not responding"
    docker-compose logs backend | tail -20
fi

# Test 2: Frontend
echo ""
echo "Test 2: Frontend (http://localhost:8080)"
FRONTEND_RESPONSE=$(curl -s http://localhost:8080/)
if echo "$FRONTEND_RESPONSE" | grep -q "SequoAlpha"; then
    echo "✅ Frontend is serving files"
else
    echo "❌ Frontend is not serving files"
fi

# Test 3: API Proxy
echo ""
echo "Test 3: API Proxy (http://localhost:8080/api/test-cors)"
PROXY_RESPONSE=$(curl -s http://localhost:8080/api/test-cors)
if echo "$PROXY_RESPONSE" | grep -q "CORS"; then
    echo "✅ API proxy is working"
else
    echo "❌ API proxy is not working"
fi

# Test 4: Database
echo ""
echo "Test 4: Database Connection"
DB_TEST=$(docker-compose exec -T postgres psql -U sequoalpha_user -d sequoalpha -c "SELECT 1;" 2>&1)
if echo "$DB_TEST" | grep -q "1 row"; then
    echo "✅ Database is accessible"
else
    echo "❌ Database is not accessible"
fi

echo ""
echo "================================"
echo "📋 Test Summary"
echo "================================"
echo ""
echo "🌐 Frontend URL: http://localhost:8080"
echo "🔧 Backend API: http://localhost:8000"
echo "💾 Database: localhost:5433"
echo ""
echo "🔐 Default Credentials:"
echo "   Admin: admin / admin123"
echo "   User: user / user123"
echo ""
echo "📝 Common Commands:"
echo "   View logs:    docker-compose logs -f"
echo "   Restart:      docker-compose restart"
echo "   Stop:         docker-compose down"
echo "   Clean start:  docker-compose down -v && docker-compose up --build -d"
echo ""
echo "✨ Open http://localhost:8080 in your browser to test!"
echo ""
