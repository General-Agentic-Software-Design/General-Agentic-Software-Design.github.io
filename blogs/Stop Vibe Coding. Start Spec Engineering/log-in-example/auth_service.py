# auth_service.py — Generated from GASD spec (TRACE: US-042)

from datetime import datetime, timedelta, timezone
import jwt
import bcrypt
from fastapi import HTTPException, status

from models import LoginRequest, SessionToken
from repositories import UserRepository

def _get_secret():
    return "super-secret-key"

class AuthService:
    """Service layer for authentication. Pattern: Service."""

    def __init__(self, user_repository: UserRepository):
        # GASD DECISION: Use Dependency Injection for all external services
        self._repo = user_repository

    def login(self, req: LoginRequest) -> SessionToken:
        # Step 1: VALIDATE req — enforced by Pydantic model from TYPE annotations

        # Step 2: Fetch user — same message on failure (anti-enumeration CONSTRAINT)
        user = self._repo.find_by_email(req.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"   # CONSTRAINT: same message always
            )

        # Step 3: Verify password — DECISION: bcrypt (cost=12), constant-time
        if not bcrypt.checkpw(req.password.encode(), user.password_hash.encode()):
            self._repo.increment_failed_attempts(user.id)  # CONSTRAINT: atomic
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"   # CONSTRAINT: same message always
            )

        # Step 4: Check account lock — INVARIANT enforced
        if user.failed_attempts >= 5:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account locked. Contact support."
            )

        # Step 5: Reset counter on success (QUESTION resolved: yes, reset)
        self._repo.reset_failed_attempts(user.id)

        # Step 6: Generate JWT — DECISION: HS256, 1-hour expiry
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
        token = jwt.encode(
            {"sub": str(user.id), "exp": expires_at},
            key=_get_secret(),
            algorithm="HS256"       # DECISION: HS256 locked in spec
        )

        # NOTE: password field is @sensitive — never referenced after step 3
        return SessionToken(token=token, expires_at=expires_at.isoformat())
