from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, JSON, Column

class AuditLogBase(SQLModel):
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", index=True)
    action: str = Field(index=True, max_length=255) # e.g., "create", "update", "delete"
    target_type: str = Field(index=True, max_length=255) # e.g., "employee", "department", "user"
    target_id: Optional[int] = Field(default=None, index=True)
    details: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)

class AuditLog(AuditLogBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class AuditLogPublic(AuditLogBase):
    id: int
    user_email: Optional[str] = None

class AuditLogsPublic(SQLModel):
    data: list[AuditLogPublic]
    count: int
