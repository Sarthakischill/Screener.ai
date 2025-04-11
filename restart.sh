#!/bin/bash

echo "🛑 Stopping all running processes..."

# Kill any running Python and Node processes
pkill -f "python3 run.py" || true
pkill -f "node.*react-scripts" || true

# Wait a moment
sleep 2

# Remove database to start fresh
echo "🗑️ Removing database for fresh start..."
rm -f job_screening.db

# Check for .env file and load API key
if [ -f ".env" ]; then
    echo "📄 Loading environment from .env file..."
    export $(grep -v '^#' .env | xargs)
fi

# Ensure GEMINI_API_KEY is set
if [ -z "$GEMINI_API_KEY" ]; then
    echo "❌ Error: GEMINI_API_KEY environment variable is not set."
    echo "Please set the API key in .env file or as an environment variable"
    exit 1
fi

# Initialize the database and import data
echo "🗄️ Initializing database..."
python3 -c "from app.models.models import init_db; init_db()"

echo "📊 Importing data..."
python3 import_data.py

# Run the application (without re-importing data)
echo "🚀 Starting application..."
# Start backend server in the background
echo "🏗️ Starting the backend server..."
python3 run.py &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to initialize..."
sleep 5

# Start frontend in the background
echo "💻 Starting the frontend..."
cd frontend
npm start &
FRONTEND_PID=$!

# Trap CTRL+C to kill all processes
trap "echo '🛑 Stopping all services...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT

# Keep the script running
echo "✅ Screener is running!"
echo "📱 Frontend: http://localhost:3000"
echo "🔌 Backend API: http://localhost:8000"
echo "Press Ctrl+C to stop all services."

# Wait for user to interrupt
wait 