from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import init_db, SessionLocal
from app.api import auth, documents, users

app = FastAPI(title="Railways HR System API", version="1.0.0", docs_url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(users.router)


@app.on_event("startup")
def startup_event():
    init_db()
    from app.models import User
    from app.core.security import hash_password
    db = SessionLocal()
    try:
        if db.query(User).count() == 0:
            db.add(User(username="admin", full_name="المدير العام", seclevel="admin", password=hash_password("admin123")))
            db.add(User(username="user", full_name="مستخدم عادي", seclevel="user", password=hash_password("user123")))
            db.commit()
            print("Users created: admin/admin123, user/user123")
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Railways HR System API", "status": "running", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "healthy"}
