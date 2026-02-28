import asyncio
from auth_service import AuthService
from models import LoginRequest
from repositories import User, UserRepository

# A simple in-memory repository for the demonstration
class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users = {
            "test@example.com": User(
                id=1,
                email="test@example.com",
                # Bcrypt hash for "password123"
                password_hash="$2b$12$Q832pT5HKw3/Xgs7J7jCgOjFmTW40YeT2mIWu2fryd/mENCXwfu6a",
                failed_attempts=0
            )
        }

    def find_by_email(self, email: str):
        return self.users.get(email)

    def increment_failed_attempts(self, user_id: int):
        for user in self.users.values():
            if user.id == user_id:
                user.failed_attempts += 1
                print(f"  [Repo] Incremented failed attempts for user {user_id} to {user.failed_attempts}")

    def reset_failed_attempts(self, user_id: int):
        for user in self.users.values():
            if user.id == user_id:
                user.failed_attempts = 0
                print(f"  [Repo] Reset failed attempts for user {user_id}")

def run_test_case(service, email, password, label):
    print(f"\n>>> Case: {label}")
    try:
        req = LoginRequest(email=email, password=password)
        result = service.login(req)
        print(f"  [Success] Token: {result.token[:20]}... (Expires: {result.expires_at})")
    except Exception as e:
        print(f"  [Error] {type(e).__name__}: {e}")

if __name__ == "__main__":
    repo = InMemoryUserRepository()
    service = AuthService(repo)

    print("--- Starting GASD Auth Service Demo ---")
    
    # 1. Successful Login
    run_test_case(service, "test@example.com", "ValidPass1!", "Correct Credentials")

    # 2. Wrong Password (should increment failure)
    run_test_case(service, "test@example.com", "WrongPass1!", "Wrong Password")

    # 3. Repeat wrong password until lockout (limit is 5)
    for i in range(4):
        run_test_case(service, "test@example.com", "WrongPass1!", f"Wrong Password Attempt {i+2}")

    # 4. Attempt login on locked account
    run_test_case(service, "test@example.com", "ValidPass1!", "Correct Credentials (but Locked)")

    print("\n--- Demo Complete ---")
