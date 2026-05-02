from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_admin
from app.core.security import (
    create_access_token,
    hash_password,
    needs_rehash,
    verify_password,
)
from app.db.database import get_db
from app.models import User
from app.schemas import Token, UserCreate, UserLogin, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(creds: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == creds.username).first()
    if not user or not verify_password(creds.password, user.password):
        raise HTTPException(status_code=401, detail="اسم المستخدم أو كلمة المرور غير صحيحة")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="الحساب غير نشط")

    if needs_rehash(user.password):
        user.password = hash_password(creds.password)
        db.commit()

    token = create_access_token(data={"sub": str(user.id), "seclevel": user.seclevel})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(user),
    }


@router.post("/register", response_model=UserResponse)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    """Create a new user. Admin-only.

    Public self-registration is intentionally disabled: the previous
    public endpoint allowed an attacker to set ``seclevel='admin'`` and
    take over the system. Use ``POST /users`` (also admin-only) for new
    users; this route is kept only as an alias for backward compatibility.
    """
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="اسم المستخدم موجود بالفعل")
    new_user = User(
        username=user.username,
        full_name=user.full_name,
        seclevel=user.seclevel if user.seclevel in {"admin", "user"} else "user",
        password=hash_password(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserResponse.model_validate(new_user)
