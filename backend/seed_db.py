#!/usr/bin/env python3
"""
Seed the database with initial data
"""
import sys
from pathlib import Path
import bcrypt

# كلمة السر التي ستخزن في قاعدة البيانات
password = "طويلة جدًا جدًا جدًا حتى تتجاوز الحد المسموح به في bcrypt"

# تقليص كلمة السر إلى 72 بايت
password = password[:72]  # تقليص الكلمة لتكون 72 بايت كحد أقصى

# الآن يمكنك تمرير الكلمة إلى bcrypt بعد التأكد من طولها
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

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
        admin.set_password("admin123")

        # Create regular user
        user = User(
            username="user",
            full_name="مستخدم عادي",
            seclevel="user"
        )
        user.set_password("user123")

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