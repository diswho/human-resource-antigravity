from typing import List, Optional
from datetime import datetime
from sqlmodel import Session, select
from app.models.attendance import AttendanceLog

def get_attendance_logs(
    session: Session, 
    *, 
    employee_id: int,
    skip: int = 0, 
    limit: int = 100,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[AttendanceLog]:
    statement = select(AttendanceLog).where(AttendanceLog.employee_id == employee_id)
    if start_date:
        statement = statement.where(AttendanceLog.timestamp >= start_date)
    if end_date:
        statement = statement.where(AttendanceLog.timestamp <= end_date)
    return session.exec(statement.offset(skip).limit(limit).order_by(AttendanceLog.timestamp.desc())).all()
