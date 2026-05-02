import os
import sys
from pathlib import Path

os.environ.setdefault("SECRET_KEY", "test-secret-key-please-do-not-use-in-prod-32+chars")
os.environ.setdefault("DATABASE_URL", "sqlite:///./_test_railways_hr.db")
os.environ.setdefault("INITIAL_ADMIN_USERNAME", "testadmin")
os.environ.setdefault("INITIAL_ADMIN_PASSWORD", "test-admin-pw-strong")
os.environ.setdefault("ALLOW_ORIGINS", "http://localhost:5173")

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.db.database import Base, engine  # noqa: E402
from app.main import _bootstrap_initial_admin, app  # noqa: E402


@pytest.fixture(scope="session")
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    _bootstrap_initial_admin()
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)
