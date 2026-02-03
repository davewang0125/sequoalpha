#!/bin/bash

# Frontend-Only Docker Test Script
# Test the frontend independently without backend

echo "🎨 SequoAlpha Frontend Docker Test"
echo "===================================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Build frontend image
echo "🔨 Building frontend Docker image..."
docker build -f Dockerfile.frontend-only -t sequoalpha-frontend-test . 2>&1 | grep -E "(Step|Successfully|ERROR)" || true

# Stop any existing container
echo ""
echo "🧹 Cleaning up existing containers..."
docker stop sequoalpha-frontend-only 2>/dev/null || true
docker rm sequoalpha-frontend-only 2>/dev/null || true

# Run frontend container
echo ""
echo "🚀 Starting frontend container..."
docker run -d \
  --name sequoalpha-frontend-only \
  -p 9000:80 \
  sequoalpha-frontend-test

# Wait for container to start
echo "⏳ Waiting for frontend to start..."
sleep 3

# Check if container is running
if docker ps | grep -q sequoalpha-frontend-only; then
    echo "✅ Frontend container is running"
else
    echo "❌ Frontend container failed to start"
    echo ""
    echo "📋 Container logs:"
    docker logs sequoalpha-frontend-only
    exit 1
fi

echo ""
echo "🧪 Testing frontend..."
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:9000/)
if [ "$RESPONSE" = "200" ]; then
    echo "✅ Frontend is responding (HTTP $RESPONSE)"
else
    echo "❌ Frontend returned HTTP $RESPONSE"
fi

echo ""
echo "================================"
echo "✨ Frontend is ready!"
echo "================================"
echo ""
echo "🌐 Frontend URL: http://localhost:9000"
echo ""
echo "📝 Note: Backend is not running in this test."
echo "   The frontend will show connection errors for API calls."
echo "   This is normal - this test is only for frontend rendering."
echo ""
echo "📝 Useful Commands:"
echo "   View logs:     docker logs -f sequoalpha-frontend-only"
echo "   Stop:          docker stop sequoalpha-frontend-only"
echo "   Remove:        docker rm sequoalpha-frontend-only"
echo "   Restart:       docker restart sequoalpha-frontend-only"
echo ""
echo "🌐 Opening frontend in browser..."
echo ""

# Try to open browser
if command -v open &> /dev/null; then
    open http://localhost:9000
elif command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:9000
else
    echo "Please open http://localhost:9000 in your browser"
fi

echo "✅ Frontend-only test complete!"
echo ""
