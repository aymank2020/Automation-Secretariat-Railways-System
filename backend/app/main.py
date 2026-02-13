from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import init_db, SessionLocal
from app.api import auth, documents, users

app = FastAPI(
    title="Railways HR System API",
    description="نظام إدارة المراسلات للسكك الحديدية",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(users.router)


@app.on_event("startup")
def startup_event():
    """Initialize database and seed on startup"""
    init_db()
    # Auto-seed if empty
    from app.models import User
    from app.core.security import get_password_hash
    db = SessionLocal()
    try:
        if db.query(User).count() == 0:
            admin = User(
                username="admin",
                full_name="المدير العام",
                seclevel="admin",
                password=get_password_hash("admin123")
            )
            user = User(
                username="user",
                full_name="مستخدم عادي",
                seclevel="user",
                password=get_password_hash("user123")
            )
            db.add(admin)
            db.add(user)
            db.commit()
            print("✅ Default users created: admin/admin123, user/user123")
    finally:
        db.close()


@app.get("/")
def read_root():
    return {
        "message": "Railways HR System API",
        "status": "running",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
