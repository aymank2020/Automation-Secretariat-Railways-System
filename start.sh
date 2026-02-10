#!/bin/bash

docker-compose down -v
docker-compose up -d --build

echo "Waiting for PostgreSQL to be ready..."
sleep 5

docker-compose exec backend python -c "from app.db.database import init_db; init_db()"

echo "✅ System is running!"
echo "Frontend: http://localhost:5173"
echo "Backend API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"