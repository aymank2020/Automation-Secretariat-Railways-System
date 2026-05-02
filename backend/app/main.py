import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, documents, users
from app.core.config import settings
from app.core.security import hash_password
from app.db.database import SessionLocal, init_db
from app.models import User

logger = logging.getLogger("railways")
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))


def _bootstrap_initial_admin() -> None:
    """Create the configured initial admin if no users exist.

    The initial password must be supplied via ``INITIAL_ADMIN_PASSWORD`` env
    var. If it is missing on a fresh database we log a warning and skip
    seeding - never fall back to a baked-in default.
    """
    db = SessionLocal()
    try:
        if db.query(User).count() > 0:
            return
        if not settings.INITIAL_ADMIN_PASSWORD:
            logger.warning(
                "Database is empty but INITIAL_ADMIN_PASSWORD is not set; "
                "no admin user was created. Set the env var and restart, "
                "or create a user manually."
            )
            return
        db.add(
            User(
                username=settings.INITIAL_ADMIN_USERNAME,
                full_name="المدير العام",
                seclevel="admin",
                password=hash_password(settings.INITIAL_ADMIN_PASSWORD),
            )
        )
        db.commit()
        logger.info("Bootstrapped initial admin user '%s'", settings.INITIAL_ADMIN_USERNAME)
    finally:
        db.close()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    _bootstrap_initial_admin()
    yield


app = FastAPI(
    title="Railways HR System API",
    version="1.1.0",
    docs_url="/docs",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "Railways HR System API", "status": "running", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "healthy"}
