from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from app.models.hr import Employee

class AttendanceLogBase(SQLModel):
    timestamp: datetime = Field(index=True)
    punch_type: str = Field(max_length=10) # 0=Check-In, 1=Check-Out etc.
    terminal_id: Optional[int] = Field(default=None)
    external_id: Optional[int] = Field(default=None, index=True) # id in att_punches

class AttendanceLog(AttendanceLogBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id")
    
    employee: Employee = Relationship(back_populates="attendance_logs")

class AttendanceSummaryBase(SQLModel):
    date: datetime = Field(index=True)
    total_hours: float = Field(default=0.0)
    overtime_hours: float = Field(default=0.0)
    status: Optional[str] = Field(default=None)

class AttendanceSummary(AttendanceSummaryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id")
