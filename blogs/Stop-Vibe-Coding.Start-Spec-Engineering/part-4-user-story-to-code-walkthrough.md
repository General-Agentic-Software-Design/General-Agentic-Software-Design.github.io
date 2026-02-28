# From User Story to Working Code — A GASD Walkthrough

> *One login feature. No ambiguity. No drift. Here's the full run.*

---

This is where theory meets practice.

We take one user story through the complete GASD lifecycle: product requirement → design spec → human review checkpoint → AI-generated code → AI-generated tests. Every decision traceable. Every test inevitable.

---

## Step 1 — The User Story

This comes from the product team. GASD doesn't replace it — it sits downstream of it.

```user-story
US-042: As a registered user, I want to log in with my email and password
so that I can access my account dashboard.

Acceptance Criteria:
  AC-1: Valid credentials return a session token valid for 1 hour
  AC-2: Invalid email or password returns a 401 Unauthorized error
  AC-3: An account is locked after 5 consecutive failed login attempts
  AC-4: A locked account returns a 403 Forbidden error
```

Clear. Business language. Notice what it *doesn't* say: JWT vs. opaque tokens, bcrypt vs. argon2, how failed attempts are tracked, what "locked" means in the database. Those are engineering decisions — correctly left open by the product team.

This is exactly where unguided AI goes wrong. Given this story as a raw prompt, every implicit engineering decision gets made differently every session.

---

## Step 2 — The GASD Spec

The architect authors the spec — closing every door the user story left open.

```gasd
CONTEXT: "REST API backend"
TARGET: "Python / FastAPI"
TRACE: "US-042", "AC-1", "AC-2", "AC-3", "AC-4"

// ── Locked Design Decisions ───────────────────────────────────────
DECISION "Token Format":
    CHOSEN: "JWT (HS256, 1-hour expiry)"
    RATIONALE: "Stateless — no session store required for MVP. Standard, well-supported."
    ALTERNATIVES: ["Opaque token (Redis-backed)", "Session cookie"]
    AFFECTS: [AuthService.login]

DECISION "Password Hashing":
    CHOSEN: "bcrypt (cost=12)"
    RATIONALE: "Adaptive cost factor, constant-time comparison, available in all target runtimes"
    AFFECTS: [AuthService.login, AuthService.register]

// ── Type Contracts ─────────────────────────────────────────────────
TYPE LoginRequest:
    email:    String @format("email") @max_length(255)
    password: String @min_length(8) @sensitive      // @sensitive: never log this field

TYPE SessionToken:
    token:      String   @sensitive
    expires_at: DateTime @standard("ISO-8601")

// ── Component Architecture ─────────────────────────────────────────
COMPONENT AuthService:
    PATTERN: "Service"
    DEPENDENCIES: [UserRepository]
    INTERFACE:
        login(req: LoginRequest) -> SessionToken

// ── Behavioral Flow ────────────────────────────────────────────────
FLOW login(req: LoginRequest) -> SessionToken:
    @error_strategy("Exception-based")
    @trace("AC-1", "AC-2", "AC-3", "AC-4")

    1. VALIDATE req
    2. ACHIEVE "Fetch user record by email" via UserRepository
        ON_ERROR: THROW UnauthorizedException("Invalid credentials")
    3. ENSURE password_matches(req.password, user.password_hash)
        OTHERWISE THROW UnauthorizedException("Invalid credentials")
    4. ENSURE user.failed_attempts < 5
        OTHERWISE THROW ForbiddenException("Account locked. Contact support.")
    5. ACHIEVE "Reset failed_attempts to 0" via UserRepository
    6. CREATE SessionToken:
        token      = GENERATE_JWT(user.id, @algorithm("HS256"))
        expires_at = NOW() + 1 hour
    7. RETURN SessionToken

// ── Global Rules ───────────────────────────────────────────────────
CONSTRAINT: "Failed login attempts MUST be incremented atomically"
CONSTRAINT: "All authentication errors MUST use the same error message to prevent user enumeration"
INVARIANT:  "A locked account (failed_attempts >= 5) MUST NOT be unlocked automatically"
```

Every acceptance criterion now has an explicit answer:

- **AC-1** → `GENERATE_JWT` + `expires_at = NOW() + 1 hour`
- **AC-2** → `THROW UnauthorizedException("Invalid credentials")` in steps 2 and 3
- **AC-3** → `CONSTRAINT: "Failed login attempts MUST be incremented atomically"`
- **AC-4** → `ENSURE user.failed_attempts < 5 OTHERWISE THROW ForbiddenException`

The anti-enumeration `CONSTRAINT` wasn't in the user story. The architect added it. That's the GASD layer's job: capturing what the product team can't reasonably be expected to specify.

---

## Step 3 — The Human Review Checkpoint

Before handing to an agent, the spec goes to review. A colleague spots a gap:

> *"When a user successfully logs in, do we reset their failed_attempts counter? The spec says accounts don't auto-unlock — but what happens to the counter on success?"*

In vibe coding: the AI guesses silently. Probably resets — it's the more common pattern — and nobody knows the decision was made.

In GASD, this becomes a formal block:

```gasd
QUESTION: "Should a successful login reset failed_attempts to 0?"
    BLOCKING: true
    CONTEXT: AuthService.login
    RAISED_BY: "Lead Architect"
```

`BLOCKING: true` — the agent will not generate code for `AuthService.login` until this is resolved.

The team decides: **yes, reset on success — non-locked accounts only.** Step 5 of the FLOW reflects it. Decision recorded, dated, traceable to US-042, version-controlled. Next quarter, when someone asks "why does login reset the counter?" — the answer is in the spec, not someone's memory.

---

## Step 4 — AI Generates the Code

```python
# auth_service.py — Generated from GASD spec (TRACE: US-042)

from datetime import datetime, timedelta, timezone
import jwt
import bcrypt
from fastapi import HTTPException, status

from .models import LoginRequest, SessionToken
from .repositories import UserRepository


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
```

Every comment traces directly to a `DECISION`, `CONSTRAINT`, or `INVARIANT` in the spec. The code isn't just correct — it's *explainable*.

---

## Step 5 — AI Generates the Tests

From the same spec, the agent generates the test suite — each test mapping directly to an acceptance criterion:

```python
# test_auth_service.py — Generated from GASD spec (TRACE: US-042)

import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException

from auth_service import AuthService
from models import LoginRequest


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
```

The developer never wrote "test that failed login returns the same message to prevent user enumeration."

The GASD `CONSTRAINT` made that test **inevitable**.

---

## What Just Happened

| Artifact | Source |
|---|---|
| `auth_service.py` | Generated from GASD spec |
| `test_auth_service.py` | Generated from same GASD spec |
| Anti-enumeration constraint | Added by architect — not in user story |
| Atomic increment guarantee | Added by architect — not in user story |
| Counter reset behavior | Resolved via `QUESTION` block |
| All decisions traceable | Every comment points back to spec |

The user story said "5 failed attempts = locked." The architect said "atomic increment, same error message, reset on success, never auto-unlock." The AI implemented and tested all of it — consistently, completely, without guessing.

That is Spec-Driven Development in practice.

---

*The spec makes right behavior inevitable. The AI fills in the blanks — it doesn't make the decisions.*

---

**Part 4 of 6** · **Previous**: [Part 3 — GASD: A Design Language](./part-3-gasd-design-language.md) · **Next**: [Part 5 — Human + AI: The New Collaboration Model](./part-5-human-ai-collaboration.md)
