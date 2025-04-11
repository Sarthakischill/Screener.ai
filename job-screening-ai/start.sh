#!/bin/bash

echo "🚀 Starting Job Screening AI..."

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed. Please install Ollama first."
    echo "Visit https://ollama.com/download for installation instructions."
    exit 1
fi

# Check if llama3 model is available in Ollama
if ! ollama list | grep -q "llama3"; then
    echo "⬇️ Downloading llama3 model for Ollama..."
    ollama pull llama3
fi

# Check if background Ollama server is running
if ! curl -s http://localhost:11434/api/tags &> /dev/null; then
    echo "🚀 Starting Ollama server..."
    ollama serve &
    OLLAMA_PID=$!
    sleep 5  # Wait for Ollama to start
fi

# Import data if no database exists
if [ ! -f "job_screening.db" ]; then
    echo "📊 Importing initial data..."
    python import_data.py
fi

# Start backend server in the background
echo "🏗️ Starting the backend server..."
python run.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Start frontend in the background
echo "💻 Starting the frontend..."
cd frontend
npm start &
FRONTEND_PID=$!

# Trap CTRL+C to kill all processes
trap "echo '🛑 Stopping all services...'; kill $BACKEND_PID $FRONTEND_PID $OLLAMA_PID 2>/dev/null; exit" INT

# Keep the script running
echo "✅ Job Screening AI is running!"
echo "📱 Frontend: http://localhost:3000"
echo "🔌 Backend API: http://localhost:8000"
echo "Press Ctrl+C to stop all services."

# Wait for user to interrupt
wait 