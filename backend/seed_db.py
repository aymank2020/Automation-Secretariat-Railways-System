#!/usr/bin/env python3
"""
Seed the database with initial data
"""
import sys
from pathlib import Path
import bcrypt

# كلمة السر التي ستخزن في قاعدة البيانات
password = "Ak@123456*"

# تحويل كلمة السر إلى بايتات، ثم تقليصها إلى 72 بايت كحد أقصى
password_bytes = password.encode('utf-8')[:72]  # تقليص كلمة السر بعد تحويلها إلى بايتات

# الآن يمكنك تمرير الكلمة إلى bcrypt بعد التأكد من طولها
hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

# الآن قد يتم تخزين hashed_password في قاعدة البيانات

# Add app to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.database import SessionLocal, init_db
from app.models import User

def seed_database():
    """Create initial admin user"""
    db = SessionLocal()

    try:
        # Create admin user
        admin = User(
            username="admin",
            full_name="المدير العام",
            seclevel="admin"
        )
        # استخدام hashed password مباشرة
        admin.password = hashed_password

        # Create regular user
        user = User(
            username="user",
            full_name="مستخدم عادي",
            seclevel="user"
        )
        # تحويل كلمة المرور إلى بايتات ومن ثم تشفيرها
        user.password = bcrypt.hashpw(b"user123"[:72], bcrypt.gensalt())

        # Add users
        db.add(admin)
        db.add(user)
        db.commit()

        print("✅ Database seeded successfully!")
        print("   Admin: admin / admin123")
        print("   User:  user / user123")

    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    seed_database()
