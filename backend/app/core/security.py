import os
import hmac
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import jwt

from .config import settings


def _pbkdf2_sha256(password: str, salt: bytes, iterations: int = 390000) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)


def get_password_hash(password: str) -> str:
    iterations = 390000
    salt = os.urandom(16)
    dk = _pbkdf2_sha256(password, salt, iterations)
    return f"pbkdf2_sha256${iterations}${salt.hex()}${dk.hex()}"


def verify_password(password: str, hashed: str) -> bool:
    try:
        scheme, iter_str, salt_hex, hash_hex = hashed.split("$")
        assert scheme == "pbkdf2_sha256"
        iterations = int(iter_str)
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(hash_hex)
        computed = _pbkdf2_sha256(password, salt, iterations)
        return hmac.compare_digest(computed, expected)
    except Exception:
        return False


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None, extra_claims: Optional[Dict[str, Any]] = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    now = datetime.now(timezone.utc)
    expire = now + expires_delta
    payload: Dict[str, Any] = {"sub": subject, "iat": int(now.timestamp()), "exp": int(expire.timestamp())}
    if extra_claims:
        payload.update(extra_claims)
    token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
    return token


def decode_access_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
