#!/bin/bash

echo "🚀 Starting SequoAlpha Backend..."
echo "🔧 Environment: $FLASK_ENV"
echo "🔧 Port: $PORT"

# Initialize the database
echo "🔧 Initializing database..."
python init_db.py

if [ $? -eq 0 ]; then
    echo "✅ Database initialization successful!"
else
    echo "❌ Database initialization failed!"
    exit 1
fi

# Start the application
echo "🚀 Starting Gunicorn server..."
gunicorn main:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --log-level info
