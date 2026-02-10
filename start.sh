#!/bin/bash

# Railway Correspondence Management System - Quick Start Script

echo "🚂 نظام إدارة المراسلات - السكك الحديدية"
echo "=============================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker غير مثبت. يرجى تثبيته أولاً"
    echo "📖 تعليمات التثبيت: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose غير مثبت"
    exit 1
fi

echo "✅ Docker و Docker Compose جاهزان"
echo ""

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo "📝 إنشاء ملف .env للباك إند..."
    cp backend/.env.example backend/.env
    echo "⚠️  يرجى تعديل backend/.env وإضافة SECRET_KEY جديد"
fi

# Start containers
echo "🐳 تشغيل الحاويات..."
docker-compose up -d

# Wait for database
echo "⏳ انتظار قاعدة البيانات..."
sleep 5

# Seed database
echo "🌱 إنشاء قاعدة البيانات والبيانات الأولية..."
docker-compose exec -T backend python seed_db.py

echo ""
echo "✅ النظام جاهز للتشغيل!"
echo ""
echo "📍 الروابط:"
echo "   - الفرونت إند: http://localhost:5173"
echo "   - الباك إند:   http://localhost:8000"
echo "   - API Docs:    http://localhost:8000/docs"
echo ""
echo "👤 بيانات الدخول:"
echo "   - Admin: admin / admin123"
echo "   - User:  user / user123"
echo ""
echo "📝 ملاحظة: يرجى تغيير كلمات المرور في بيئة الإنتاج!"
echo ""
echo "⏹️  لإيقاف النظام: docker-compose down"