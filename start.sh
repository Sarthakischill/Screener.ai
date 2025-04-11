#!/bin/bash

echo "🚀 Starting Job Screening AI with Gemini API..."

# Check for .env file and load API key
if [ -f ".env" ]; then
    echo "📄 Loading environment from .env file..."
    export $(grep -v '^#' .env | xargs)
fi

# Check if Gemini API key is provided as argument or already set from .env
if [ -z "$GEMINI_API_KEY" ] && [ -z "$1" ]; then
    echo "❌ Error: Gemini API key is required."
    echo "Usage: ./start.sh YOUR_GEMINI_API_KEY"
    echo "Or create a .env file with GEMINI_API_KEY=YOUR_KEY"
    exit 1
elif [ -n "$1" ]; then
    # Override with command line if provided
    export GEMINI_API_KEY="$1"
fi

echo "✅ Gemini API key set."

# Import data
echo "📊 Importing data from job_description.csv and CVs1 folder..."
python3 import_data.py

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
echo "✅ Job Screening AI is running!"
echo "📱 Frontend: http://localhost:3000"
echo "🔌 Backend API: http://localhost:8000"
echo "Press Ctrl+C to stop all services."

# Wait for user to interrupt
wait 