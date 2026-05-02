#!/usr/bin/env bash
# Local-development launcher. Runs the backend (uvicorn) and the frontend
# (vite) in foreground, with safe defaults for SECRET_KEY and INITIAL_ADMIN.
# For production, use docker-compose.prod.yml instead.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

echo "=== نظام إدارة المراسلات - السكك الحديدية (dev) ==="

if [ ! -f backend/.env ]; then
    echo "📝 Generating backend/.env (dev defaults)..."
    SECRET=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
    cat > backend/.env <<EOF
DATABASE_URL=sqlite:///./railways_hr.db
SECRET_KEY=${SECRET}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
ALLOW_ORIGINS=http://localhost:5173
INITIAL_ADMIN_USERNAME=admin
INITIAL_ADMIN_PASSWORD=$(python3 -c 'import secrets; print(secrets.token_urlsafe(16))')
UPLOAD_DIR=./uploads
EOF
    echo "   Generated dev creds in backend/.env (do NOT use in production)."
fi

# --- Backend ---
echo "📦 Installing backend dependencies..."
( cd backend && pip install -q -r requirements.txt )

echo "🚀 Starting backend on http://localhost:8000"
( cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload ) &
BACKEND_PID=$!

# --- Frontend ---
echo "📦 Installing frontend dependencies..."
( cd frontend && npm install --silent )

echo "🚀 Starting frontend on http://localhost:5173"
( cd frontend && npx vite --host 0.0.0.0 --port 5173 ) &
FRONTEND_PID=$!

trap 'kill ${BACKEND_PID} ${FRONTEND_PID} 2>/dev/null; exit 0' INT TERM

wait
