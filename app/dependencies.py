import secrets

from fastapi import Security, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import settings

bearer_scheme = HTTPBearer()


def require_admin(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
):
    """
    Validates the bearer token against the stored admin token.
    Uses constant-time comparison to prevent timing attacks.
    """
    if not secrets.compare_digest(
        credentials.credentials.encode("utf-8"),
        settings.ADMIN_TOKEN.encode("utf-8"),
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized.",
        )
