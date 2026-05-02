import hashlib
from datetime import UTC, datetime, timedelta

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError
from jose import JWTError, jwt

from app.core.config import settings

_ph = PasswordHasher()


def hash_password(password: str) -> str:
    """Hash a password with Argon2id."""
    return _ph.hash(password)


def _verify_legacy_sha256(plain: str, hashed: str) -> bool:
    """Verify the legacy salt$sha256 format that earlier versions used.

    Kept only so existing users can log in once after upgrade; on success
    the caller should rehash via `hash_password` and persist the new value.
    """
    try:
        salt, pw_hash = hashed.split("$", 1)
    except ValueError:
        return False
    return hashlib.sha256((salt + plain).encode()).hexdigest() == pw_hash


def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not hashed_password:
        return False
    if hashed_password.startswith("$argon2"):
        try:
            return _ph.verify(hashed_password, plain_password)
        except (VerifyMismatchError, InvalidHashError):
            return False
    return _verify_legacy_sha256(plain_password, hashed_password)


def needs_rehash(hashed_password: str) -> bool:
    if not hashed_password.startswith("$argon2"):
        return True
    try:
        return _ph.check_needs_rehash(hashed_password)
    except InvalidHashError:
        return True


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None
