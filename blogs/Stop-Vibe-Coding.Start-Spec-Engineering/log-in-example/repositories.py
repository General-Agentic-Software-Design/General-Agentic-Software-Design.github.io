from abc import ABC, abstractmethod
from pydantic import BaseModel

class User(BaseModel):
    id: int
    email: str
    password_hash: str
    failed_attempts: int

class UserRepository(ABC):
    @abstractmethod
    def find_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def increment_failed_attempts(self, user_id: int):
        pass

    @abstractmethod
    def reset_failed_attempts(self, user_id: int):
        pass
