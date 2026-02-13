# نظام إدارة المراسلات - السكك الحديدية

## التشغيل

### Backend
```
cd backend
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```
http://localhost:8000 — API Docs: http://localhost:8000/docs

### Frontend
```
cd frontend
npm install
npm run dev
```
http://localhost:5173

## الدخول
- **admin** / **admin123** (مدير)
- **user** / **user123** (مستخدم)
