import re

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserSchema(BaseModel):
    email: EmailStr = Field(pattern=r".+@example\.com$")
    first_name: str = Field(min_length=2, frozen=True)
    last_name: str = Field(min_length=2, frozen=True)
    password: str = Field(..., min_length=8, max_length=64)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[\W]", value):
            raise ValueError("Password must contain at least one special character.")
        return value


class UserSerializer(UserSchema):
    class Config:
        from_attributes = True


class UserSchemaUpdate(BaseModel):
    first_name: str = Field(min_length=2, frozen=True)
    last_name: str = Field(min_length=2, frozen=True)
    password: str = Field(..., min_length=8, max_length=64)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[\W]", value):
            raise ValueError("Password must contain at least one special character.")
        return value
