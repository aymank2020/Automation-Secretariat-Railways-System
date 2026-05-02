"""Idempotent admin-bootstrap helper.

This is normally not needed at runtime - the FastAPI lifespan handler
already bootstraps the initial admin on first startup if the DB is empty
and ``INITIAL_ADMIN_PASSWORD`` is set in the env.

Kept for operators who want to (re-)seed manually:

    python seed_db.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.core.config import settings  # noqa: E402
from app.core.security import hash_password  # noqa: E402
from app.db.database import SessionLocal, init_db  # noqa: E402
from app.models import User  # noqa: E402


def main() -> int:
    init_db()
    db = SessionLocal()
    try:
        if db.query(User).count() > 0:
            print("Already seeded; nothing to do.")
            return 0
        if not settings.INITIAL_ADMIN_PASSWORD:
            print(
                "INITIAL_ADMIN_PASSWORD is not set; refusing to create a default admin.",
                file=sys.stderr,
            )
            return 1
        db.add(
            User(
                username=settings.INITIAL_ADMIN_USERNAME,
                full_name="المدير العام",
                seclevel="admin",
                password=hash_password(settings.INITIAL_ADMIN_PASSWORD),
            )
        )
        db.commit()
        print(f"Seeded admin user '{settings.INITIAL_ADMIN_USERNAME}'.")
        return 0
    finally:
        db.close()


if __name__ == "__main__":
    raise SystemExit(main())
