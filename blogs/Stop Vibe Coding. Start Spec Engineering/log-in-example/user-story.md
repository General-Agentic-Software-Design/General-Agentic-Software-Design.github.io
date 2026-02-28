
# Step 1 — The User Story
US-042: As a registered user, I want to log in with my email and password
so that I can access my account dashboard.

# Acceptance Criteria
- **AC-1:** Valid credentials return a session token valid for 1 hour
- **AC-2:** Invalid email or password returns a 401 Unauthorized error
- **AC-3:** An account is locked after 5 consecutive failed login attempts
- **AC-4:** A locked account returns a 403 Forbidden error
