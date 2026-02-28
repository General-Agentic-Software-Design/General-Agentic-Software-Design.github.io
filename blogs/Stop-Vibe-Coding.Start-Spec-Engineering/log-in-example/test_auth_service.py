
# test_auth_service.py — Generated from GASD spec (TRACE: US-042)

import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException

from auth_service import AuthService
from models import LoginRequest
from repositories import User

def valid_user(failed_attempts=0):
    return User(
        id=1,
        email="a@b.com",
        password_hash="$2b$12$Q832pT5HKw3/Xgs7J7jCgOjFmTW40YeT2mIWu2fryd/mENCXwfu6a",
        failed_attempts=failed_attempts
    )


@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def service(mock_repo):
    return AuthService(user_repository=mock_repo)


# AC-1: Valid credentials return a session token valid for 1 hour
def test_login_success_returns_token(service, mock_repo):
    mock_repo.find_by_email.return_value = valid_user(failed_attempts=0)
    result = service.login(LoginRequest(email="a@b.com", password="ValidPass1!"))
    assert result.token is not None
    assert "expires_at" in result.__dict__

# AC-2: Invalid email returns 401 with generic message
def test_login_unknown_email_returns_401(service, mock_repo):
    mock_repo.find_by_email.return_value = None
    with pytest.raises(HTTPException) as exc:
        service.login(LoginRequest(email="x@y.com", password="ValidPass1!"))
    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid credentials"  # CONSTRAINT: no enumeration

# AC-2: Wrong password returns 401 with IDENTICAL message (anti-enumeration)
def test_login_wrong_password_returns_401_same_message(service, mock_repo):
    mock_repo.find_by_email.return_value = valid_user(failed_attempts=0)
    with pytest.raises(HTTPException) as exc:
        service.login(LoginRequest(email="a@b.com", password="WrongPassword1!"))
    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid credentials"  # Same message — CONSTRAINT verified

# AC-3 / AC-4: Locked account returns 403
def test_login_locked_account_returns_403(service, mock_repo):
    mock_repo.find_by_email.return_value = valid_user(failed_attempts=5)
    with pytest.raises(HTTPException) as exc:
        service.login(LoginRequest(email="a@b.com", password="ValidPass1!"))
    assert exc.value.status_code == 403
    assert "locked" in exc.value.detail.lower()

# INVARIANT: locked account is never auto-unlocked
def test_locked_account_not_auto_unlocked(service, mock_repo):
    mock_repo.find_by_email.return_value = valid_user(failed_attempts=5)
    with pytest.raises(HTTPException):
        service.login(LoginRequest(email="a@b.com", password="ValidPass1!"))
    mock_repo.reset_failed_attempts.assert_not_called()  # INVARIANT enforced

# QUESTION resolved: successful login resets failed_attempts
def test_successful_login_resets_failed_attempts(service, mock_repo):
    mock_repo.find_by_email.return_value = valid_user(failed_attempts=3)
    service.login(LoginRequest(email="a@b.com", password="ValidPass1!"))
    mock_repo.reset_failed_attempts.assert_called_once()
