"""
User entity for database operations.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UserEntity(Base):
    """
    User entity representing the user table in the database.

    Attributes:
        id: Primary key.
        email: User's email address (unique).
        first_name: User's first name.
        last_name: User's last name.
        password: User's hashed password.
    """

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)

    def __repr__(self) -> str:
        return f"<UserEntity(id={self.id}, email={self.email})>"

    def to_dict(self) -> dict:
        """Convert entity to dictionary."""
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "password": self.password,
        }
