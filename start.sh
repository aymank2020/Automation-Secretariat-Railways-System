#!/bin/bash
echo "=== نظام إدارة المراسلات - السكك الحديدية ==="
echo ""

# Backend
echo "📦 Installing backend dependencies..."
cd backend
pip install -r requirements.txt
echo ""

echo "🗄️ Initializing database..."
python seed_db.py
echo ""

echo "🚀 Starting backend on http://localhost:8000"
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

# Frontend
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
echo ""

echo "🚀 Starting frontend on http://localhost:5173"
npx vite --host 0.0.0.0 --port 5173 &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ System is running!"
echo "   Frontend: http://localhost:5173"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "   Login: admin / admin123"
echo ""
echo "Press Ctrl+C to stop..."

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" SIGINT SIGTERM
wait
