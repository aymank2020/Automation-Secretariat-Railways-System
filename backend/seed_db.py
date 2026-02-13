#!/usr/bin/env python3
"""
Seed the database with initial data
"""
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.db.database import SessionLocal, init_db
from app.models import User
from app.core.security import get_password_hash


def seed_database():
    """Create initial admin and user accounts"""
    db = SessionLocal()

    try:
        # Check if already seeded
        existing = db.query(User).filter(User.username == "admin").first()
        if existing:
            print("⚠️ Database already seeded! Skipping...")
            return

        # Create admin user
        admin = User(
            username="admin",
            full_name="المدير العام",
            seclevel="admin",
            password=get_password_hash("admin123")
        )

        # Create regular user
        user = User(
            username="user",
            full_name="مستخدم عادي",
            seclevel="user",
            password=get_password_hash("user123")
        )

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
