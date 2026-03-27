import base64

from cryptography.fernet import Fernet

from app.core.config import get_settings


def _get_fernet() -> Fernet:
    settings = get_settings()
    if not settings.encryption_key:
        raise ValueError("ENCRYPTION_KEY is required")
    key = settings.encryption_key.encode("utf-8")
    try:
        return Fernet(key)
    except ValueError:
        # Fallback for raw 32-byte keys in env.
        key = base64.urlsafe_b64encode(settings.encryption_key.encode("utf-8").ljust(32, b"0")[:32])
        return Fernet(key)


def encrypt_secret(value: str) -> str:
    return _get_fernet().encrypt(value.encode("utf-8")).decode("utf-8")


def decrypt_secret(value: str) -> str:
    return _get_fernet().decrypt(value.encode("utf-8")).decode("utf-8")
