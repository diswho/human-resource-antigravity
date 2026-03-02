from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship

from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    hr = "hr"
    employee = "employee"

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    role: UserRole = Field(default=UserRole.employee, index=True)
    full_name: Optional[str] = Field(default=None, max_length=255)
    employee_id: Optional[int] = Field(default=None, foreign_key="employee.id")

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)

class UserUpdate(UserBase):
    email: Optional[str] = Field(default=None, max_length=255)
    password: Optional[str] = Field(default=None, min_length=8, max_length=40)
    role: Optional[UserRole] = None

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    
    employee: Optional["Employee"] = Relationship(back_populates="user")

class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(SQLModel):
    sub: Optional[int] = None
