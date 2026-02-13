import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from app.db.database import SessionLocal, init_db
from app.models import User
from app.core.security import hash_password

init_db()
db = SessionLocal()
if db.query(User).count() == 0:
    db.add(User(username="admin", full_name="المدير العام", seclevel="admin", password=hash_password("admin123")))
    db.add(User(username="user", full_name="مستخدم عادي", seclevel="user", password=hash_password("user123")))
    db.commit()
    print("Done: admin/admin123, user/user123")
else:
    print("Already seeded")
db.close()
