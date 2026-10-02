from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.database import get_db
from app.models import User

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)) -> User:
    payload = decode_access_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Token غير صالح")
    try:
        user_id = int(payload.get("sub"))
    except (TypeError, ValueError, OverflowError):
        raise HTTPException(status_code=401, detail="Token غير صالح")
    if user_id <= 0:
        raise HTTPException(status_code=401, detail="Token غير صالح")
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="المستخدم غير موجود")
    return user


def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.seclevel != "admin":
        raise HTTPException(status_code=403, detail="مسموح للمدير فقط")
    return current_user
